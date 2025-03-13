'''
Title: ingestion.py
Author: Clayton Bennett
Created: 13 March 2025

Purpose: Take all raw submissions and convert to hourly structured submissions.
Provide a template to be filled.
'''
import pandas as pd
import json
from datetime import datetime
import schedule
import time

def ingest_data(intermediate_export_filename):
    # Parse JSON data

    json_data = json.loads(data)

    # Create DataFrame
    df = pd.DataFrame(json_data)

    # Convert timestamps to datetime objects
    df['timestamp_entry_ISO'] = pd.to_datetime(df['timestamp_entry_ISO'])
    df['timestamp_intended_ISO'] = pd.to_datetime(df['timestamp_intended_ISO'])

    # Group data by hour
    df.set_index('timestamp_entry_ISO', inplace=True)
    df_hourly = df.resample('H').mean()

    # Fill NaN values with 0
    df_hourly.fillna(0, inplace=True)

    # Save the structured data to a CSV file
    df_hourly.to_csv('structured_data.csv')

    print("Ingestion complete. Structured data saved to 'structured_data.csv'.")

def scheduled_run():
# Schedule the ingestion to run every hour
intermediate_export_filename
structured_export_filename = 'structured_data.csv'
schedule.every().hour.do(ingest_data(intermediate_export_filename))

print("Scheduler started. Ingestion will run every hour.")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == "__main__":
    hourly_basin_clarifiers_window()

"""
Other values that are calculated:
RAS
Underflow
RAS = underflow- total WAS

"""