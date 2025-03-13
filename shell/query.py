from pathlib import Path
from datetime import datetime
import os

BATCH_DIR = Path("./batch")

def run_query():
    """
    Runs an interactive tutorial to generate a batch script.
    """
    print("\n=== Welcome to the Interactive Dungeon Design! ===")
    print("Let's create a custom batch script step by step.")
    print("You can always type 'done' to finish the tutorial.")

    # Ensure the batch directory exists
    if not BATCH_DIR.exists():
        BATCH_DIR.mkdir(parents=True)

    # Prompt for a batch file name
    batch_file_name = input("Enter a name for your batch script (e.g., dungeon_adventure.txt): ").strip()
    if batch_file_name == "done":
        print("Exiting tutorial. No batch script was created.")
        return
    
    batch_file_path = BATCH_DIR / batch_file_name

    # Initialize the batch script content
    commands = []

    # Interactive question flow
    while True:
        print("\nWhat would you like to add to your batch script?")
        print("1. Spoof Hourly Data")
        print("2. Spoof Daily Summary")
        print("3. List Export Directory")
        print("4. Clear Export Directory")
        print("5. Custom Command")
        print("6. Finish and Save Script")
        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            # Add a spoof_hourly command
            current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")  # Current time in ISO format
            print(f"Suggested timestamp (current time): {current_time}")
            timestamp = input(f"Enter a timestamp or press Enter to accept [{current_time}]: ").strip()
            timestamp = timestamp if timestamp else current_time

            flow_rate = input("Enter a flow rate (e.g., 120.5): ").strip()
            cod = input("Enter a COD value (e.g., 38.1): ").strip()
            water_quality = input("Enter water quality (e.g., good): ").strip()
            commands.append(f"spoof_hourly {timestamp} {flow_rate} {cod} {water_quality}")
        elif choice == "2":
            # Add a spoof_daily command
            date = input("Enter a date (YYYY-MM-DD): ").strip()
            clarifier_status = input("Enter clarifier status (e.g., operational): ").strip()
            observations = input("Enter observations: ").strip()
            commands.append(f"spoof_daily {date} {clarifier_status} {observations}")
        elif choice == "3":
            # Add a list_exports command
            commands.append("list_exports")
        elif choice == "4":
            # Add a clear_exports command
            commands.append("clear_exports")
        elif choice == "5":
            # Add a custom command
            custom_command = input("Enter your custom command: ").strip()
            commands.append(custom_command)
        elif choice == "6":
            # Finish the script and save it
            break
        else:
            print("Invalid choice. Please select a valid option.")

    # Write the commands to the batch file
    with open(batch_file_path, "w") as batch_file:
        for command in commands:
            batch_file.write(command + "\n")

    print(f"\nBatch script saved to: {batch_file_path}")
    print("You can now run it from the shell using the batch command!")
    return os.path.basename(batch_file_path)