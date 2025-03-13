# __main__.py
from gui.gui import menu_window

def cli_entry():
    try:
        # Launch the gui
        menu_window() 
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    cli_entry()