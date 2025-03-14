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
from collections import defaultdict
from app.directories import Directories

def parse_json(data):
    """Parses JSON data."""
    return json.loads(data)

def convert_timestamps(data):
    """Converts timestamp strings to datetime objects."""
    for entry in data:
        if entry['timestamp_entry_ISO'] is not None:
            entry['timestamp_entry_ISO'] = datetime.strptime(entry['timestamp_entry_ISO'], "%Y-%m-%dT%H:%M:%S")
        
        if entry['timestamp_intended_ISO'] is not None:
            entry['timestamp_intended_ISO'] = datetime.strptime(entry['timestamp_intended_ISO'], "%Y-%m-%dT%H:%M:%S")
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
                hourly_data[hour].update(entry)
            else:
                for key, value in entry.items():
                    if key not in ['timestamp_entry_ISO', 'timestamp_intended_ISO', 'operator'] and value is not None:
                        hourly_data[hour][key] = value
    
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
            entry['timestamp_ISO'] = entry['timestamp__ISO'].isoformat()
    return data

def save_to_json(data, filename):
    """Saves the structured data to a JSON file."""
    # Convert datetime objects to strings
    data = serialize_datetimes(data)
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def ingest_data(intermediate_export_filename, structured_export_filename):
    # Load JSON data from the file
    with open(intermediate_export_filename, 'r') as file:
        data = file.read()
    
    # Parse JSON data
    json_data = parse_json(data)

    # Convert timestamps to datetime objects
    json_data = convert_timestamps(json_data)

    # Group data by hour
    hourly_data = group_by_hour(json_data)

    # Fill NaN values with 0
    filled_data = fill_na(hourly_data)

    # Save the structured data to a JSON file
    save_to_json(filled_data, structured_export_filename)

    print("Ingestion complete. Structured data saved to 'structured_data.csv'.")

def scheduled_run():
    # Schedule the ingestion to run every hour
    intermediate_export_filenames_hourly = (Directories.EXPORT_DIR /"basin_clarifier_hourly_data.json", Directories.EXPORT_DIR /"hourly_data.json")
    structured_export_filename = Directories.EXPORT_DIR /'structured_data.json'
    for f in intermediate_export_filenames_hourly:
        print(f)
        schedule.every().hour.do(ingest_data(f,structured_export_filename))

    print("Scheduler started. Ingestion will run every hour.")

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_now():
    # Run ingestion now
    intermediate_export_filenames_hourly = (Directories.EXPORT_DIR / "basin_clarifier_hourly_data.json", Directories.EXPORT_DIR / "hourly_data.json")
    structured_export_filename = Directories.EXPORT_DIR / 'structured_data.json'
    for f in intermediate_export_filenames_hourly:
        print(f)
        ingest_data(f,structured_export_filename)

if __name__ == "__main__":
    scheduled_run()

"""
Other values that are calculated:
RAS
Underflow
RAS = underflow- total WAS

"""