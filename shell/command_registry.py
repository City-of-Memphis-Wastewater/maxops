from shell.batch_processor import process_batch
from app.utils.helpers import list_export_files, clear_export_directory

import subprocess
from pathlib import Path
import requests
import json

def run_webapp(shell_instance, args):
    """
    Runs the FastAPI web app in development mode.

    Args:
        shell_instance: An instance of the cmd2 shell.
        args: Command-line arguments (if any).
    """
    print("Starting the FastAPI web app...")
    try:
        subprocess.run(["uvicorn", "app.main:app", "--reload"], check=True)
    except KeyboardInterrupt:
        print("\nWeb app stopped by user.")
    except Exception as e:
        print(f"Error starting the web app: {e}")


def spoof_hourly(shell_instance, args):
    """
    Sends fake hourly data for testing.

    Args:
        shell_instance: An instance of the cmd2 shell.
        args: Command-line arguments in the format:
              "timestamp flow_rate cod water_quality"
    """
    try:
        parts = args.split()
        if len(parts) != 4:
            print("Usage: spoof_hourly <timestamp> <flow_rate> <cod> <water_quality>")
            return

        timestamp, flow_rate, cod, water_quality = parts
        data = {
            "timestamp": timestamp,
            "flow_rate": float(flow_rate),
            "cod": float(cod),
            "water_quality": water_quality,
        }

        response = requests.post("http://localhost:8000/submit-hourly", data=data)
        print(f"Server response: {response.json()}")
    except Exception as e:
        print(f"Error spoofing hourly data: {e}")


def spoof_daily(shell_instance, args):
    """
    Sends fake daily summary data for testing.

    Args:
        shell_instance: An instance of the cmd2 shell.
        args: Command-line arguments in the format:
              "date clarifier_status observations"
    """
    try:
        parts = args.split(",", 2)
        if len(parts) != 3:
            print("Usage: spoof_daily <date>,<clarifier_status>,<observations>")
            return

        date, clarifier_status, observations = parts
        data = {
            "date": date.strip(),
            "clarifier_status": clarifier_status.strip(),
            "observations": observations.strip(),
        }

        response = requests.post("http://localhost:8000/submit-daily", data=data)
        print(f"Server response: {response.json()}")
    except Exception as e:
        print(f"Error spoofing daily data: {e}")


def list_exports(shell_instance, args):
    """
    Lists all files in the exports directory.

    Args:
        shell_instance: An instance of the cmd2 shell.
        args: Command-line arguments (if any).
    """
    files = list_export_files()
    if files:
        print("Export files:")
        for file in files:
            print(f"- {file}")
    else:
        print("Export directory does not exist or is empty.")


def clear_exports(shell_instance, args):
    """
    Clears all files in the exports directory.

    Args:
        shell_instance: An instance of the cmd2 shell.
        args: Command-line arguments (if any).
    """
    if clear_export_directory():
        print("Export directory cleared.")
    else:
        print("Export directory does not exist or was already empty.")


def batch(shell_instance, args):
    """
    Executes commands from a batch script file located in the batch directory.

    Args:
        shell_instance: An instance of the cmd2 shell.
        args: Command-line arguments (batch file name).
    """
    if not args.strip():
        print("Usage: batch <batch_file_name>")
    else:
        process_batch(args.strip(), shell_instance)


def tutorial(shell_instance, args):
    """
    Launches the interactive tutorial.

    Args:
        shell_instance: An instance of the cmd2 shell.
        args: Command-line arguments (if any).
    """
    from shell.tutorial import run_tutorial
    run_tutorial()


def query(shell_instance, args):
    """
    Launches the interactive query tool for generating batch scripts.

    Args:
        shell_instance: An instance of the cmd2 shell.
        args: Command-line arguments (if any).
    """
    from shell.query import run_query
    run_query()


def register_commands(shell_instance):
    """
    Registers custom commands to the given shell instance.

    Args:
        shell_instance: An instance of the cmd2 shell.
    """
    # Attach custom commands to the shell instance
    shell_instance.do_run_webapp = run_webapp
    shell_instance.do_spoof_hourly = spoof_hourly
    shell_instance.do_spoof_daily = spoof_daily
    shell_instance.do_list_exports = list_exports
    shell_instance.do_clear_exports = clear_exports
    shell_instance.do_batch = batch
    shell_instance.do_tutorial = tutorial
    shell_instance.do_query = query
