def run_tutorial():
    """
    Interactive tutorial to teach new users about the shell features, PowerShell scripts, 
    and the functionality of the web app.
    """
    print("\n=== Welcome to the Interactive Tutorial for Your Project ===")
    print("In this tutorial, you'll learn about:")
    print("1. The commands available in the shell")
    print("2. The PowerShell scripts provided")
    print("3. The functionality of the web app")
    print("\nYou can type 'next' to proceed or 'exit' to leave the tutorial at any point.\n")

    # Step 1: Introduction to Shell Commands
    input("Step 1: Learn about the shell commands. Press Enter to continue...")
    print("""
The shell provides the following commands:
- run_webapp: Starts the web app using uvicorn in development mode.
- spoof_hourly: Sends fake hourly data to the app for testing.
- spoof_daily: Sends fake daily summary data for testing.
- list_exports: Lists files in the exports directory.
- clear_exports: Deletes files in the exports directory.
- batch: Executes batch scripts to automate workflows.
- tutorial: Launches this tutorial to guide users.
\n""")
    input("Type 'next' to proceed...")

    # Step 2: Explanation of PowerShell Scripts
    print("\nStep 2: Learn about the PowerShell scripts.")
    print("""
The following PowerShell scripts are available:
1. setup_environment.ps1: Sets up the project's directories and installs dependencies.
2. run_webapp.ps1: Launches the web app in development mode.
3. spoof_hourly.ps1: Sends sample hourly data to the app.
4. execute_batch.ps1: Processes batch scripts in the batch/ directory.
5. manage_exports.ps1: Lists or clears files in the exports directory.
6. generate_sample_batch.ps1: Creates a sample batch script for testing.
7. test_api.ps1: Sends test requests to the web app's endpoints.
\n""")
    input("Type 'next' to proceed...")

    # Step 3: Walkthrough of Web App Functionality
    print("\nStep 3: Explore the web app's functionality.")
    print("""
The web app allows you to:
- Submit hourly data through a form at /overview-hourly-form.
- Submit daily summaries through a form at /daily-form.
- View recent submissions using the /api/recent-hourly endpoint.
- Manage exported files, generated in the exports/intermediate directory.

To access the web app:
1. Start the app using 'run_webapp' in the shell or run_webapp.ps1.
2. Open your browser and go to http://localhost:8000.
3. Use the available forms and endpoints to interact with the app.
\n""")
    input("Type 'next' to proceed...")

    # Step 4: Integration with Batch Scripts
    print("\nStep 4: Using Batch Scripts for Automation.")
    print("""
Batch scripts in the batch/ directory allow you to automate tasks. 
For example:
- Spoof data entries at specific times.
- List or clear export directories after completing workflows.

To execute a batch script:
1. Create a batch script using 'generate_sample_batch.ps1' or manually.
2. Run it using the 'batch' command in the shell.

Example:
batch afternoon_workflow.txt
\n""")
    input("Type 'next' to proceed...")

    print("=== Tutorial Complete ===")
    print("You're now ready to start using the project!")
    print("Type 'tutorial' in the shell anytime to relaunch this tutorial.\n")
