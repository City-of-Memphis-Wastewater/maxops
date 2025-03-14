import cmd2
import os
import subprocess
from pathlib import Path
import requests
import argparse
import json
import pprint
from datetime import datetime
import ast
import operator
import readline
import inspect
#from directories import Directories

from shell.query import run_query  # Import the tutorial function
from shell.tutorial import run_tutorial  # Import the tutorial function
from shell.batch_processor import process_batch  # Import batch processing function

import app.utils.helpers as helpers
import app.utils.ingestion as ingestion

# Path configuration for your project
EXPORT_DIR = Path("./exports/intermediate")

class HistoryEntry:
    """Custom history item to store and display commands properly."""
    def __init__(self, command: str):
        self.command = command.strip()  # Ensure no trailing or leading whitespace

    def pr(self, idx: int, script: bool = False, expanded: bool = False, verbose: bool = False) -> str:
        """Format history for printing, ensuring clean and consistent output."""
        return f"{idx}: {self.command}"

    def __str__(self):
        return f"{'-'}: {self.command}"
        #return self.command

class ShellApp(cmd2.Cmd):
    """Interactive shell for testing, spoofing, and running the web app."""
    maxops_prettytitle = '''
     __  __             ___
    |  \/  | __ ___  __/ _ \ _ __  ___
    | |\/| |/ _` \ \/ / | | | '_ \/ __|
    | |  | | (_| |>  <| |_| | |_) \__ \\
    |_|  |_|\__,_/_/\_\\____/| .__/|___/
                            |_|

    '''
    def __init__(self):
        super().__init__()
        self.prompt = "maxops> "
        self.intro = r"{}".format(self.maxops_prettytitle) + \
        '''
        Welcome to the MaxOps Shell.
        Type "help" to see available commands.
        Type "gui" to launch the graphical user interface.
        Type "run_webapp" to launch the web app.
        '''
        self.vars = {}
        self.modules = {}
        self.context = {'self': self,
                        'pprint': pprint.pprint,
                        'list': list,
                        'str': str,
                        'int': int,
                        'float': float,
                        'dict': dict,
                        'dir': dir,
                        #'set': set,  # I don't genereally use sets anyway, and set is a functon in cmd2
                        'tuple': tuple,
                        'len': len,
                        'sum': sum,
                        'min': min,
                        'max': max,
                        'sorted': sorted,
                        'type': type,
                        'range': range,
                        'enumerate': enumerate,
                        'zip': zip,
                        'map': map,
                        'filter': filter,
                        'any': any,
                        'all': all,
                        'abs': abs,
                        'round': round,
                        'repr': repr,}
        #print("ShellApp initialized!")

        self.debug = True  # Set the default debug value to True
        
        # Set startup script - if the file does not exist, there will be problems
        # self.startup_script = os.path.join(os.path.dirname(__file__), "startup.txt")

        # Store command history
        history_dir = os.path.join(os.path.dirname(__file__), 'history')
        os.makedirs(history_dir, exist_ok=True)  # Ensure the directory exists
        self.persistent_history_file = os.path.join(history_dir, 'shell_history.txt')

        # Auto-load history from the file if it exists
        if os.path.exists(self.persistent_history_file):
            self._load_history()

    def _load_history(self):
        """Load commands from the persistent history file at startup."""
        try:
            if os.path.exists(self.persistent_history_file):
                with open(self.persistent_history_file, 'r', encoding='utf-8') as history_file:
                    for line in history_file:
                        command = line.strip()
                        if command:
                            self.history.append(HistoryEntry(command))  
                            readline.add_history(command)
                print(f"Loaded {len(self.history)} commands from history.")
            else:
                print("No history file found, starting with an empty history.")
        except Exception as e:
            self.perror(f"Error loading history: {e}")

    
    def postcmd(self, stop, statement):
        """Called after every command to append it to the history file."""
        try:
            full_command = statement.raw.strip()
            if full_command:
                with open(self.persistent_history_file, 'a', encoding='utf-8') as history_file:
                    history_file.write(full_command + '\n')

                self.history.append(HistoryEntry(full_command))  # Store properly
            else:
                print("Skipped saving empty or invalid command.")
        except Exception as e:
            self.perror(f"Error saving command to history: {e}")
        return stop
    
    # === Command: Clear ===
    def do_clear(self,line):
        "Clear the window."
        try:
            os.system("cls")
        except:
            os.system("clear")

    # === Command: About ===
    def do_about(self,line):
        "Show the MaxOps prettty title"
        print(self.maxops_prettytitle)
    
    # === Command: Run Web App ===
    run_webapp_parser = argparse.ArgumentParser(description="Run the FastAPI web app.")
    @cmd2.with_argparser(run_webapp_parser)
    def do_run_webapp(self, args):
        """Start the FastAPI web app (in development mode)."""
        try:
            print("Starting the web app...")
            subprocess.run(["uvicorn", "app.main:app", "--reload"], check=True)
        except KeyboardInterrupt:
            print("\nWeb app stopped by user.")
        except Exception as e:
            print(f"Error starting the web app: {e}")
    
    # If no args are provided for a command, call this generalized function to return help  
    def print_help_if_no_args(self,args,func_name):
        keys_to_remove = ['cmd2_statement', 'cmd2_handler']
        args_dict = {key: value for key, value in vars(args).items() if key not in keys_to_remove}
        if all(value is None for value in args_dict.values()):
            getattr(self, func_name)("--help")  # Dynamically call the method
            return
        
    def post_data_or_save_locally(self,html_template,data,local_save_function,source_description):
        if data is not None:
            try:
                response = requests.post(f"http://localhost:8000/{html_template}", data=data)
                print(f"Server response: {response.json()}")
            except Exception as e:
                print(f"Error spoofing {source_description} data: {e}")
                print("Web app not running, defaulting to local export.")
                local_save_function(data)

    # === Command: Spoof Overview (Flows and COD) Hourly Data ===
    overview_hourly_parser = argparse.ArgumentParser(description="Spoof hourly data for testing.")
    overview_hourly_parser.add_argument("-t","--timestamp", type=str, default=None, help="Timestamp in ISO format, e.g., 2025-03-05T08:00:00. It you use '-t now', or don't include one, the ISO timestamp for now will be generated. If you use '-t 13', the time will be submitted as today at 1 PM,  for example; this input must be an integrer.")
    overview_hourly_parser.add_argument("-i","--influent_flow_rate_MGD", type=float, default=None, help="Hourly influent flow.")
    overview_hourly_parser.add_argument("-a","--after_wet_well_flow_rate_MGD", type=float, default=None, help="Hourly after-wet-well flow.")
    overview_hourly_parser.add_argument("-e","--effluent_flow_rate_MGD", type=float, default=None, help="Hourly effluent flow.")
    #overview_hourly_parser.add_argument("-r","--ras_flow_rate_MGD", type=float, default=None, help="Hourly RAS flow.") # calculated from entries in clarifier page
    overview_hourly_parser.add_argument("-w","--was_flow_rate_MGD", type=float, default=None, help="Hourly WAS flow.")
    overview_hourly_parser.add_argument("-c","--cod_predisinfection_mgPerLiter", type=float, default=None, help="Hourly prefinal COD (chemical oxygen demand) concentration (mgPerLiter) (~150).")
    overview_hourly_parser.add_argument("-op","--operator", type=str, default=None, help="Operator indentifier.")
    #overview_hourly_parser.add_argument("-u","--underflow_rate_MGD", type=float, default=None, help="Hourly influent flow.") # calculated from entries in clarifier page
    @cmd2.with_argparser(overview_hourly_parser)
    def do_overview_hourly(self, args):
        """Spoof Overview hourly data and send it to the API."""
        func_name = inspect.currentframe().f_code.co_name
        source_description = "overview hourly"
        local_save_function = helpers.local_save_data_overview_hourly
        html_template = "submit-hourly"
        self.print_help_if_no_args(args,func_name) # Print help if no args are provided
        """Capure args as data dictionary."""
        try:
            # if you chanage these keys and the order, and a relevant CSV file already exists, you should see: "WARNING: The existing CSV column names DO NOT match data.keys()"
            data = {
                "timestamp_entry_ISO": helpers.nowtime(),
                "timestamp_intended_ISO": helpers.sanitize_time(args.timestamp),
                "influent_flow_rate_MGD":args.influent_flow_rate_MGD,
                "after_wet_well_flow_rate_MGD":args.after_wet_well_flow_rate_MGD,
                "effluent_flow_rate_MGD":args.effluent_flow_rate_MGD,
                "was_flow_rate_MGD":args.was_flow_rate_MGD,
                "cod_predisinfection_mgPerLiter":args.cod_predisinfection_mgPerLiter,
                "operator":args.operator,
                "source": "local-shell-Python-cmd2"
            }
        except Exception as e:
            print(f"Error spoofing {source_description} data: {e}")
            data = None
        self.post_data_or_save_locally(html_template,data,local_save_function,source_description)

    # === Command: copy Spoof Hourly Data ===
    basin_clarifier_flows_parser = argparse.ArgumentParser(description="Spoof hourly data for testing.\nRun this command: batch basin_clarifier_flows.txt to test / save time.")
    basin_clarifier_flows_parser.add_argument("-t","--timestamp", type=str, default=None, help="Timestamp in ISO format, e.g., 2025-03-05T08:00:00. It you use '-t now', or don't include one, the ISO timestamp for now will be generated. If you use '-t 13', the time will be submitted as today at 1 PM,  for example; this input must be an integrer.")
    basin_clarifier_flows_parser.add_argument("-op","--operator", type=str, default=None, help="Operator indentifier.")
    basin_clarifier_flows_parser.add_argument("-nb1","--north_basin_1_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-nb3","--north_basin_3_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-nb5","--north_basin_5_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-nb7","--north_basin_7_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-nb9","--north_basin_9_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-nb11","--north_basin_11_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-nb13","--north_basin_13_MGD", type=float, default=None, help="Flow (MGD)")

    basin_clarifier_flows_parser.add_argument("-sb1","--south_basin_1_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-sb3","--south_basin_3_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-sb5","--south_basin_5_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-sb7","--south_basin_7_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-sb9","--south_basin_9_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-sb11","--south_basin_11_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-sb13","--south_basin_13_MGD", type=float, default=None, help="Flow (MGD)")

    basin_clarifier_flows_parser.add_argument("-nc1","--north_clarifier_1_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-nc2","--north_clarifier_2_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-nc3","--north_clarifier_3_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-nc4","--north_clarifier_4_MGD", type=float, default=None, help="Flow (MGD)")

    basin_clarifier_flows_parser.add_argument("-sc1","--south_clarifier_1_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-sc2","--south_clarifier_2_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-sc3","--south_clarifier_3_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-sc4","--south_clarifier_4_MGD", type=float, default=None, help="Flow (MGD)")

    basin_clarifier_flows_parser.add_argument("-nr1","--north_ras_1_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-nr2","--north_ras_2_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-nr3","--north_ras_3_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-nr4","--north_ras_4_MGD", type=float, default=None, help="Flow (MGD)")

    basin_clarifier_flows_parser.add_argument("-sr1","--south_ras_1_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-sr2","--south_ras_2_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-sr3","--south_ras_3_MGD", type=float, default=None, help="Flow (MGD)")
    basin_clarifier_flows_parser.add_argument("-sr4","--south_ras_4_MGD", type=float, default=None, help="Flow (MGD)")

    @cmd2.with_argparser(basin_clarifier_flows_parser)
    def do_spoof_basin_clarifier_flows(self, args):
        """
        Spoof basin and clarifier hourly data and send it to the API.
        """
        self.help = "Run this command: batch spoof_basin_clarifier_flows.txt to test / save time."
        func_name = inspect.currentframe().f_code.co_name
        source_description = "basin_clarifier_hourly"
        local_save_function = helpers.local_save_data_basin_clarifier_hourly
        html_template = "submit-basin-clarifier-hourly"
        self.print_help_if_no_args(args,func_name) # Print help if no args are provided
        """Capure args as data dictionary."""
        try:
            # if you chanage these keys and the order, and a relevant CSV file already exists, you should see: "WARNING: The existing CSV column names DO NOT match data.keys()"
            data = {
                "timestamp_entry_ISO": helpers.nowtime(),
                "timestamp_intended_ISO": helpers.sanitize_time(args.timestamp),
                "operator":args.operator,
                "source": "local-shell-Python-cmd2",

                "north_basin_1_MGD": args.north_basin_1_MGD,
                "north_basin_3_MGD":args.north_basin_3_MGD,
                "north_basin_5_MGD":args.north_basin_5_MGD,
                "north_basin_7_MGD":args.north_basin_7_MGD,
                "north_basin_9_MGD":args.north_basin_9_MGD,
                "north_basin_11_MGD":args.north_basin_11_MGD,
                "north_basin_13_MGD":args.north_basin_13_MGD,

                "south_basin_1_MGD":args.south_basin_1_MGD,
                "south_basin_3_MGD":args.south_basin_3_MGD,
                "south_basin_5_MGD":args.south_basin_5_MGD,
                "south_basin_7_MGD":args.south_basin_7_MGD,
                "south_basin_9_MGD":args.south_basin_9_MGD,
                "south_basin_11_MGD":args.south_basin_11_MGD,
                "south_basin_13_MGD":args.south_basin_13_MGD,

                "north_clarifier_1_MGD":args.north_clarifier_1_MGD,
                "north_clarifier_2_MGD":args.north_clarifier_2_MGD,
                "north_clarifier_3_MGD":args.north_clarifier_3_MGD,
                "north_clarifier_4_MGD":args.north_clarifier_4_MGD,

                "south_clarifier_1_MGD":args.south_clarifier_1_MGD,
                "south_clarifier_2_MGD":args.south_clarifier_2_MGD,
                "south_clarifier_3_MGD":args.south_clarifier_3_MGD,
                "south_clarifier_4_MGD":args.south_clarifier_4_MGD,

                "north_ras_1_MGD":args.north_ras_1_MGD,
                "north_ras_2_MGD":args.north_ras_2_MGD,
                "north_ras_3_MGD":args.north_ras_3_MGD,
                "north_ras_4_MGD":args.north_ras_4_MGD,

                "south_ras_1_MGD":args.south_ras_1_MGD,
                "south_ras_2_MGD":args.south_ras_2_MGD,
                "south_ras_3_MGD":args.south_ras_3_MGD,
                "south_ras_4_MGD":args.south_ras_4_MGD

            }
        except Exception as e:
            print(f"Error spoofing {source_description} data: {e}")
            data = None
        self.post_data_or_save_locally(html_template,data,local_save_function,source_description)

    # === Command: Spoof Daily Data ===
    spoof_daily_parser = argparse.ArgumentParser(description="Spoof daily data for testing.")
    spoof_daily_parser.add_argument("-t","--timestamp", type=str, default=None, help="Timestamp in ISO format, e.g., 2025-03-05T08:00:00")
    spoof_daily_parser.add_argument("-c","--clarifier_status", type=str, default=None, help="Clarifier status (e.g., operational, under maintenance).")
    spoof_daily_parser.add_argument("-o","--observations", type=str, default=None, help="Daily observations.")
    spoof_daily_parser.add_argument("-op","--operator", type=str, default=None, help="Operator indentifier.")
    @cmd2.with_argparser(spoof_daily_parser)
    def do_spoof_daily(self, args):
        """Spoof daily summary data and try to send it to the API."""
        func_name = inspect.currentframe().f_code.co_name
        source_description = "daily"
        local_save_function = helpers.local_save_data_daily
        html_template = "submit-daily"
        self.print_help_if_no_args(args,func_name) # Print help if no args are provided
        try:
            # if you chanage these keys and the order, and a relevant CSV file already exists, you should see: "WARNING: The existing CSV column names DO NOT match data.keys()"
            data = {
                "timestamp_entry_ISO": helpers.nowtime(),
                "timestamp_intended_ISO": helpers.sanitize_time(args.timestamp),
                "clarifier_status": args.clarifier_status,
                "observations": args.observations,
                "operator": args.operator,
                "source": "local-shell-Python-cmd2"
            }
        except Exception as e:
            print(f"Error spoofing {source_description} data: {e}")
            data = None
        self.post_data_or_save_locally(html_template,data,local_save_function,source_description)

    # === Command: Outfall Data Entry ===
    outfall_parser = argparse.ArgumentParser(description= "Outfall data entry.")
    outfall_parser.add_argument("-t","--timestamp", type=str, default=None, help="Timestamp in ISO format, e.g., 2025-03-05T08:00:00")
    outfall_parser.add_argument("-safe","--safe_to_make_observation", type=int, default=None, help="Outfall observation, yes[1] or no[0].")
    outfall_parser.add_argument("-float","--floatable_present", type=int, default=None, help="Outfall observation, yes[1] or no[0].")
    outfall_parser.add_argument("-scum","--scum_present", type=int, default=None, help="Outfall observation, yes[1] or no[0].")
    outfall_parser.add_argument("-foam","--foam_present", type=int, default=None, help="Outfall observation, yes[1] or no[0].")
    outfall_parser.add_argument("-oil","--oil_present", type=int, default=None, help="Outfall observation, yes[1] or no[0].")
    outfall_parser.add_argument("-op","--operator", type=str, default=None, help="Operator indentifier.")
    @cmd2.with_argparser(outfall_parser)
    def do_spoof_outfall_daily(self,args):
        """Spoof outfall daily data and send it to the API."""
        func_name = inspect.currentframe().f_code.co_name
        source_description = "outfall"
        local_save_function = helpers.local_save_data_outfall
        html_template = "submit-outfall"
        self.print_help_if_no_args(args,func_name) # Print help if no args are provided
        try:
            # if you chanage these keys and the order, and a relevant CSV file already exists, you should see: "WARNING: The existing CSV column names DO NOT match data.keys()"
            data = {
                "timestamp_entry_ISO": helpers.nowtime(),
                "timestamp_intended_ISO": helpers.sanitize_time(args.timestamp),
                "safe_to_make_observation": bool(args.safe_to_make_observation),
                "floatable_present": bool(args.floatable_present),
                "scum_present": bool(args.scum_present),
                "foam_present": bool(args.foam_present),
                "oil_present": bool(args.oil_present),
                "operator": args.operator,
                "source": "local-shell-Python-cmd2"
            }            
        except Exception as e:
            print(f"Error spoofing {source_description} data: {e}")
            data = None
        self.post_data_or_save_locally(html_template,data,local_save_function,source_description)
    
    # === Command: List Export Files ===
    def do_list_exports(self, args):
        """List files in the export directory."""
        try:
            if EXPORT_DIR.exists():
                for file in EXPORT_DIR.iterdir():
                    print(f"Export file: {file.name}")
            else:
                print("Export directory does not exist.")
        except Exception as e:
            print(f"Error listing export files: {e}")

    # === Command: Clear Export Files ===
    clear_exports_parser = argparse.ArgumentParser(description="Clear all files in the export directory.")
    @cmd2.with_argparser(clear_exports_parser)
    def do_clear_exports(self, args):
        """Clear all files in the export directory."""
        try:
            if EXPORT_DIR.exists():
                for file in EXPORT_DIR.iterdir():
                    file.unlink()
                    print(f"Deleted: {file.name}")
                print("Export directory cleared.")
            else:
                print("Export directory does not exist.")
        except Exception as e:
            print(f"Error clearing export files: {e}")
    
    # === Command: Execute Batch Script ===
    # Add batch command
    batch_parser = argparse.ArgumentParser(description="Batch process files in /batch/.")
    batch_parser.add_argument("-l","--list", type=bool, nargs="?", default=False, const=True, help="Provide flag to see list of batch files in /batch/")
    batch_parser.add_argument("-f","--file", type=str, help="Provide entire path or assume /batch/")
    @cmd2.with_argparser(batch_parser)
    def do_batch(self, args):
        """Execute commands from a batch script located in the batch directory."""
        if args.list is True:
            batchpath = "./batch/"
            onlyfiles = [f for f in os.listdir(batchpath) if os.path.isfile(os.path.join(batchpath, f))]
            print(onlyfiles)
        elif args.file is not None:
            batch_file_name = args.file
            if not batch_file_name:
                print("Usage: batch <batch_file_name>")
            else:
                process_batch(batch_file_name, self)
            
    # === Command: Test Recent Hourly Data ===
    test_recent_hourly_parser = argparse.ArgumentParser(description="Test the /api/recent-hourly endpoint.")
    @cmd2.with_argparser(test_recent_hourly_parser)
    def do_test_recent_hourly(self, args):
        """Test the /api/recent-hourly endpoint."""
        try:
            response = requests.get("http://localhost:8000/api/recent-hourly")
            data = response.json()
            print(json.dumps(data, indent=4))
        except Exception as e:
            print(f"Error testing recent hourly data: {e}")

    # === Command: Test Recent Daily Data ===
    test_recent_daily_parser = argparse.ArgumentParser(description="Test the /api/daily-summaries endpoint.")
    @cmd2.with_argparser(test_recent_daily_parser)
    def do_test_recent_daily(self, args):
        """Test the /api/daily-summaries endpoint."""
        try:
            response = requests.get("http://localhost:8000/api/daily-summaries")
            data = response.json()
            print(json.dumps(data, indent=4))
        except Exception as e:
            print(f"Error testing recent daily data: {e}")

    # === Command: Quit Shell ===
    quit_parser = argparse.ArgumentParser(description="Quit the shell.")
    @cmd2.with_argparser(quit_parser)
    def do_quit(self, args):
        """Exit the shell."""
        print("Exiting the shell. Goodbye!")
        return True
        
    # === Command: Query Guidance ===
    query_parser = argparse.ArgumentParser(description="Run query guidance, to generate a batch script.")
    @cmd2.with_argparser(query_parser)
    def do_query(self, args):
        """Exit the shell."""
        batch_filename=run_query()
        print("The query guidance is complete :)")
        return None
        
    # === Command: Tutorial ===
    tutorial_parser = argparse.ArgumentParser(description="Run tutorial, to better undestand the MaxOps program.")
    @cmd2.with_argparser(tutorial_parser)
    def do_tutorial(self, args):
        """Run the tutorial."""
        run_tutorial()
        print("The tutorial is complete!")
        #self.do_quit()
        return None
    
    # === Command: Now Time ===
    now_parser = argparse.ArgumentParser(description="Print Now time, to be easily copied or assigned to a spoof input.")
    @cmd2.with_argparser(now_parser)
    def do_now(self, args):
        """Calculate the current time."""
        now_time = helpers.nowtime()
        #print(f"{now_time}")
        self.poutput(f"{now_time}")
        #return None

    # === Command: print ===
    def do_print(self, args):
        if args:
            self.poutput(f"{args}")
        else:
            self.poutput("")

    def do_show(self, _):
        """Show all variables."""
        for key, value in self.vars.items():
            self.poutput(f"{key} = {value}")

    def do_eval(self, args):
        """Evaluate an expression using stored variables."""
        try:
            expr = self._substitute_vars(args)
            #result = self._safe_eval(expr, {**self.context,**self.vars})
            result = self._safe_eval(expr, self.context)
            self.poutput(f"{args} = {result}")
        except Exception as e:
            self.poutput(f"Error evaluating expression: {str(e)}")

    def _substitute_vars(self, expression):
        """Substitute variables in the expression with their values."""
        while True:
            original_expression = expression
            for key, value in self.vars.items():
                expression = expression.replace(f"${key}", value)
                expression = expression.replace(key, value)
            # Break if no more substitutions are happening
            if expression == original_expression:
                break
        return expression

    def _safe_eval(self, expression, context):
        """Safely evaluate an expression using ast and operator modules."""
        # Define allowed operators
        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.BitXor: operator.xor,
            ast.USub: operator.neg,
        }

        def _eval(node, context):
            if isinstance(node, ast.Constant):  # <number>
                return node.n
            elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
                return allowed_operators[type(node.op)](_eval(node.left, context), _eval(node.right, context))
            elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
                return allowed_operators[type(node.op)](_eval(node.operand, context))
            elif isinstance(node, ast.Name):  # <variable>
                return context[node.id]
            elif isinstance(node, ast.Attribute):  # <object.attribute>
                value = _eval(node.value, context)
                return getattr(value, node.attr)
            elif isinstance(node, ast.Call):  # <function call>
                func = _eval(node.func, context)
                args = [_eval(arg, context) for arg in node.args]
                return func(*args)
            elif isinstance(node, ast.Subscript):  # <variable>[<index>]
                value = _eval(node.value, context)
                if isinstance(node.slice, ast.Index):
                    index = _eval(node.slice.value, context)
                else:
                    index = _eval(node.slice, context)
                return value[index]
            else:
                raise TypeError(node)

        node = ast.parse(expression, mode='eval').body
        return _eval(node, context)
    

    def do_sett_hold(self, args):
        """Set a custom variable: set_var <name> <value>"""
        try:
            name, value = args.split()
            self.vars[name] = value
            self.poutput(f"Variable '{name}' set to '{value}'")
        except ValueError:
            self.perror("Usage: set_var <name> <value>")

    def do_sett(self, args):
        """Set a custom variable: sett <name>=<value> or sett <name> <value>"""
        try:
            # Check if the input contains an equals sign
            if '=' in args:
                name, value = args.split('=', 1)  # Split only at the first '='
            else:
                name, value = args.split(maxsplit=1)  # Split by whitespace if no '='

            # Optional: Handle parentheses as part of the value
            value = value.strip()  # Remove surrounding whitespace
            if value.startswith('(') and value.endswith(')'):
                value = value  # Keep parentheses intact, or process as needed

            self.vars[name] = value
            self.poutput(f"Variable '{name}' set to '{value}'")
        except ValueError:
            self.perror("Usage: sett <name>=<value> or sett <name> <value>")

    

        
    def default_hold(self, statement):
        """Override the default method to handle dollar sign variables."""
        # Replace variables in the command with their values
        command = statement.raw 
        for var_name, var_value in self.vars.items():
            command = command.replace(f"${var_name}", var_value)

        # Execute the modified command
        #self.poutput(f"Executing command: {command}")
        self.poutput(f"{command}")
        # You could further process the command here if needed.

    def default_test(self, statement):
        """Override the default method to handle unknown commands and undefined variables."""
        command = statement.raw

        # Handle undefined variables
        try:
            for var_name in self.vars.keys():
                if f"${var_name}" in command:
                    command = command.replace(f"${var_name}", self.vars[var_name])
            
            # Check for any remaining undefined variables
            if "$" in command:
                self.poutput("Undefined variables detected!")
        except Exception as e:
            self.perror(f"{command} failed: {e}")
            print(f"{command} is not a recognized command, alias, or macro.")

    def do_gett_hold(self, args):

        """Get a custom variable: gett <name>"""
        if isinstance(args, list):
            args = ' '.join(args)  # Convert list to a space-separated string
        value = self.vars.get(args, None)
        if value is not None:
            self.poutput(f"Variable '{args}' = '{value}'")
        else:
            self.perror(f"Variable '{args}' not found.")

    def do_gett(self, statement):
        """Get a custom variable: gett <name>"""
        var_name = statement.arg_list[0] if statement.arg_list else None  # Get the first argument as the variable name
        if var_name is None:
            self.perror("Usage: gett <name>")
            return
        
        value = self.vars.get(var_name, None)
        if value is not None:
            self.poutput(f"Variable '{var_name}' = '{value}'")
        else:
            self.perror(f"Variable '{var_name}' not found.")

    def do_gui(self,args):
        "Launch the MaxOp Graphical User Interface"
        from gui.gui import menu_window
        menu_window() 

    def do_ingest(self,args):
        "Ingest data from predefined filename set in ingestion.py."
        ingestion.IntermediateExport.run_now()



if __name__ == "__main__":

    app = ShellApp()
    app.cmdloop()
