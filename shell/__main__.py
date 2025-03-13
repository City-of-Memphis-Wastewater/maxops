# __main__.py
from shell.shell import ShellApp

def cli_entry():
    try:
        # Launch the cmd2 terminal
        app = ShellApp()
        app.cmdloop()  
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    cli_entry()
