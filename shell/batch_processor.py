from pathlib import Path

BATCH_DIR = Path("./batch")

def process_batch(batch_file_name, shell_instance):
    """
    Processes a batch file and executes its commands in the given shell instance.

    Args:
        batch_file_name (str): Name of the batch file to execute.
        shell_instance: An instance of the cmd2 shell to execute commands.
    """
    batch_file_path = BATCH_DIR / batch_file_name

    if not batch_file_path.exists():
        print(f"Batch file not found: {batch_file_path}")
        return

    try:
        print(f"Processing batch script: {batch_file_name}")
        with open(batch_file_path, "r") as batch_file:
            command = ""
            for line in batch_file:

                if not(line.strip().endswith('+')) and command =="":
                    #print("c0")
                    command = line.strip()
                    # Skip empty lines and comments (lines starting with #)
                    if command and not command.startswith("#"):
                        print(f"Executing: {command}")
                        shell_instance.onecmd(command)  # Execute the command in the shell context
                        command = ""
                    elif not command.startswith("#"):
                        command = ""
                elif line.strip().endswith('+'):
                    #print("c1")
                    wait = True
                    command = command+" "+line.strip().replace("+","")
                    #print(f"command = {repr(command)}")
                elif not(line.strip().endswith('+')) and command !="":
                    #print("c2")
                    command = command+" "+line.strip()
                    if command and not command.startswith("#"):
                        print(f"Executing: {command}")
                        shell_instance.onecmd(command)  # Execute the command in the shell context
                        command = ""
                    elif command.startswith("#"):
                        command = ""
    except Exception as e:
        print(f"Error processing batch script: {e}")
