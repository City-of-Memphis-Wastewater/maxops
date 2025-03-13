import json
import os
import FreeSimpleGUI as sg

def load_data_from_json(file_path):
    """Loads data from a JSON file."""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    else:
        sg.popup_error(f"File '{file_path}' not found!")
        return []

def create_table_layout(data):
    """Creates a table layout from the loaded JSON data."""
    # Define headers based on the keys of the first entry, if data exists
    if data:
        headers = list(data[0].keys())
        values = [[entry[key] for key in headers] for entry in data]
    else:
        headers = ["No Data Found"]
        values = []
    return headers, values

def known_window(json_file, layout_title, window_label):
    data = load_data_from_json(json_file)
    # Define the layout for the PySimpleGUI window
    layout = make_layout(data, layout_title)
    # Create the window
    window = sg.Window(window_label, layout, resizable=True)
    # Event loop
    while True:
        event, _ = window.read()
        if event == sg.WINDOW_CLOSED or event == "Close":
            break
        elif event == "Refresh":
            # Reload data on refresh
            data = load_data_from_json(json_file)
            headers, table_data = create_table_layout(data)
            window["-TABLE-"].update(values=table_data)
    window.close()


def make_layout(data,layout_title):
    
    # Create headers and table data
    headers, table_data = create_table_layout(data)

    # Get the screen size
    screen_width, screen_height = sg.Window.get_screen_size()
    layout = [
        [sg.Text(layout_title, font=("Helvetica", 16))],
        [sg.Column(
            [[sg.Table(
                values=table_data,
                headings=headers,
                justification="center",
                auto_size_columns=True,
                #col_widths=[len(header) - 2 for header in headers],
                #col_widths=[int(screen_width / len(headers)) - 10 for _ in headers],  # Adjust column widths dynamically
                display_row_numbers=True,
                num_rows=20,
                key="-TABLE-",
                enable_events=True  # Enables interaction events
            )]],
            scrollable=True,
            #horizontal_scroll=True,  # Enables horizontal scrolling
            #size=(800, 400)  # Adjust size as needed
            size=(screen_width - 50, 400)  # Full-width adjustment
        )],
        [sg.Button("Refresh"), sg.Button("Close")]
    ]
    return layout

if __name__ == "__main__":
    json_file = os.path.join("exports","intermediate" ,"outfall_daily_data.json")
    layout_title = "Daily Outfall Data Submissions"
    window_label = "Outfall Data Viewer"
    known_window(json_file, layout_title, window_label)
