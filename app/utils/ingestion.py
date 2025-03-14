'''
Title: ingestion.py
Author: Clayton Bennett
Created: 13 March 2025

Purpose: Take all raw submissions and convert to hourly structured submissions.
Provide a template to be filled.
'''
#import numpy as np
#import pandas as pd
import json
from datetime import datetime
#import schedule
import time
import pprint
from collections import defaultdict
from app.directories import Directories

def parse_json(data):
    """Parses JSON data."""
    return json.loads(data)

def convert_timestamps(data):
    """Converts timestamp strings to datetime objects."""
    for entry in data:
        if 'timestamp_entry_ISO' in entry and entry['timestamp_entry_ISO'] is not None:
            entry['timestamp_entry_ISO'] = datetime.strptime(entry['timestamp_entry_ISO'], "%Y-%m-%dT%H:%M:%S")
        if 'timestamp_intended_ISO' in entry and entry['timestamp_intended_ISO'] is not None:
            entry['timestamp_intended_ISO'] = datetime.strptime(entry['timestamp_intended_ISO'], "%Y-%m-%dT%H:%M:%S")
        if 'timestamp_ISO' in entry and entry['timestamp_ISO'] is not None:
            #print(f"entry = {entry}")
            entry['timestamp_ISO'] = datetime.strptime(entry['timestamp_ISO'], "%Y-%m-%dT%H:%M:%S")
    return data

def group_by_hour_(data):
    """Groups data by hour and keeps the most recent values."""
    hourly_data = defaultdict(lambda: {})
    for entry in data:
        if entry['timestamp_entry_ISO'] is not None:
            hour = entry['timestamp_entry_ISO'].replace(minute=0, second=0, microsecond=0)
            # Store the most recent entry for each hour
            if hour not in hourly_data or entry['timestamp_entry_ISO'] > hourly_data[hour]['timestamp_entry_ISO']:
                hourly_data[hour] = entry

    # Convert the defaultdict to a regular list of dictionaries
    result = [value for value in hourly_data.values()]
    
    return result

def group_by_hour(data):
    """Groups data by hour, keeps the most recent values, and includes a list of all operators."""
    hourly_data = defaultdict(lambda: {'operators': []})
    
    for entry in data:
        if entry['timestamp_entry_ISO'] is not None:
            hour = entry['timestamp_entry_ISO'].replace(minute=0, second=0, microsecond=0)
            # Add operator to the list of operators
            #if 'operator' in entry and entry['operator'] is not None:
            if 'operator' in entry:
                hourly_data[hour]['operators'].append(entry['operator'])
            # Store the most recent entry for each hour
            #print(entry)
            #if hour not in hourly_data or entry['timestamp_entry_ISO'] > hourly_data[hour].get('timestamp_entry_ISO', datetime.min):
            #    hourly_data[hour].update(entry)

            # Store the most recent non-null entry for each hour
            if hour not in hourly_data:
                hourly_data[hour] = {key: None for key in entry.keys()}  # Ensure all keys are initialized
                hourly_data[hour].update(entry)
            else:
                for key, value in entry.items():
                    #if key not in ['timestamp_entry_ISO', 'timestamp_intended_ISO', 'operator'] and value is not None:
                    if entry[key] is not None or hourly_data[hour].get(key) is None:
                        #hourly_data[hour][key] = value
                        hourly_data[hour][key] = entry[key]
    
    # Convert the defaultdict to a regular list of dictionaries
    result = []
    for hour, data in hourly_data.items():
        data['timestamp_ISO'] = hour.isoformat()
        data.pop('timestamp_entry_ISO', None)
        data.pop('timestamp_intended_ISO', None)
        data.pop('source', None)
        data.pop('operator', None)
        result.append(data)
    
    return result


def fill_na(data):
    """Fills NaN values with 0."""
    for entry in data:
        for key, value in entry.items():
            if value is None:
                entry[key] = 0
    return data
def serialize_datetimes(data):
    """Converts datetime objects back to strings."""
    for entry in data:
        if isinstance(entry['timestamp_ISO'], datetime):
            entry['timestamp_ISO'] = entry['timestamp_ISO'].isoformat()
    return data

def save_to_json(data, filename):
    """Saves the structured data to a JSON file."""
    # Convert datetime objects to strings
    data = serialize_datetimes(data)
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


class IntermediateExport:
    dict_intermediate_export_objects = None
    @classmethod
    def make_dict_intermediate_export_objects(cls):
        cls.dict_intermediate_export_objects = {}
    @classmethod
    def update_dict_intermediate_export_objects(cls,key,filename_semistructured,filename_structured):
            ie_o = IntermediateExport(
                key,
                filename_semistructured = filename_semistructured,
                filename_structured = filename_structured)

            cls.dict_intermediate_export_objects.update({key:ie_o})

    def __init__(self,key,filename_semistructured,filename_structured):
        self.key = key
        self.filename_semistructured = filename_semistructured
        self.filename_structured = filename_structured
    @staticmethod
    def ingest_data_to_structure(key,intermediate_export_filename, structured_export_filename):
        # Load JSON data from the file
        with open(intermediate_export_filename, 'r') as file:
            data = file.read()
        
        # Parse JSON data
        json_data = parse_json(data)

        # Convert timestamps to datetime objects
        json_data = convert_timestamps(json_data)

        # Load existing structured data
        try:
            with open(structured_export_filename, 'r') as file:
                existing_data = json.load(file)
                existing_data = convert_timestamps(existing_data)
                #pprint.pprint(existing_data)
        except FileNotFoundError:
            existing_data = []

        # Determine the most recent hour in existing data
        if existing_data:
            latest_timestamp = max(entry['timestamp_ISO'] for entry in existing_data)
            if isinstance(latest_timestamp,str):
                latest_timestamp = datetime.strptime(latest_timestamp, "%Y-%m-%dT%H:%M:%S")
        else:
            latest_timestamp = datetime.min

        # Filter new data to only include entries after the latest timestamp
        new_data = [entry for entry in json_data if entry['timestamp_entry_ISO'] > latest_timestamp]

        # Group new data by hour
        hourly_data = group_by_hour(new_data)

        # Merge new data with existing data
        combined_data = {}

        # Add existing data to the combined dictionary
        for entry in existing_data:
            timestamp = entry['timestamp_ISO']
            if isinstance(timestamp, str):
                timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
            combined_data[timestamp] = entry

        # Add new hourly data, overwriting existing entries for the same hour
        for entry in hourly_data:
            timestamp = entry['timestamp_ISO']
            if isinstance(timestamp, str):
                timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
            combined_data[timestamp] = entry

        # Convert the combined data back to a list
        combined_data_list = list(combined_data.values())

        # Fill NaN values with 0
        #filled_data = fill_na(combined_data_list)

        # Save the structured data to a JSON file
        save_to_json(combined_data_list, structured_export_filename)
        #save_to_json(filled_data, structured_export_filename)

        print(f"Ingestion complete for {key}.")

    @staticmethod
    def scheduled_run():
        # Schedule the ingestion to run every hour
        intermediate_export_filenames_hourly = (Directories.EXPORT_DIR /"basin_clarifier_hourly_data.json", Directories.EXPORT_DIR /"flows_and_cod_hourly_data.json")
        intermediate_export_filenames_hourly = (Directories.EXPORT_DIR /"flows_and_cod_hourly_data.json")
        structured_export_filename = Directories.EXPORT_DIR /'structured_data.json'
        for f in intermediate_export_filenames_hourly:
            #print(f)
            schedule.every().hour.do(ingest_data(f,structured_export_filename))

        print("Scheduler started. Ingestion will run every hour.")

        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(1)

    @staticmethod
    def run_now():
        # Run ingestion now
        # how can i find all instances of a class in python
        IntermediateExport.make_dict_intermediate_export_objects()
        IntermediateExport.update_dict_intermediate_export_objects(
            key = "basin_clarifier_hourly",
            filename_semistructured = Directories.EXPORT_DIR / "basin_clarifier_hourly_data.json",
            filename_structured = Directories.EXPORT_DIR / 'basin_clarifier_hourly_structured_data.json'
            )
        IntermediateExport.update_dict_intermediate_export_objects(
            key = "flows_and_cod_hourly",
            filename_semistructured = Directories.EXPORT_DIR / "flows_and_cod_hourly_data.json",
            filename_structured = Directories.EXPORT_DIR / 'flows_and_cod_hourly_structured_data.json'
            )
        IntermediateExport.update_dict_intermediate_export_objects(
            key = "outfall_daily",
            filename_semistructured = Directories.EXPORT_DIR / "outfall_daily_data.json",
            filename_structured = Directories.EXPORT_DIR / 'outfall_daily_structured_data.json'
            )
        for ie_o in IntermediateExport.dict_intermediate_export_objects.values():
            #ingest_data_to_structure(ie_o.filename_semistructured,ie_o.filename_structured)
            IntermediateExport.ingest_data_to_structure(ie_o.key,ie_o.filename_semistructured,ie_o.filename_structured)
            print(f"{ie_o.filename_semistructured} ingested to {ie_o.filename_structured}")
        
        #intermediate_export_filenames_hourly = (Directories.EXPORT_DIR / "basin_clarifier_hourly_data.json", Directories.EXPORT_DIR / "flows_and_cod_hourly_data.json")
        #structured_export_filename = Directories.EXPORT_DIR / 'structured_data.json'
        #for f in intermediate_export_filenames_hourly:
        #    print(f)
        #    ingest_data(f,structured_export_filename)

if __name__ == "__main__":
    IntermediateExport.scheduled_run()

"""
Other values that are calculated:
RAS
Underflow
RAS = underflow- total WAS

"""