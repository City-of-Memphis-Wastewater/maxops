import requests
import FreeSimpleGUI as sg
import app.utils.helpers as helpers

def hourly_basin_clarifiers_window():
    default_time = helpers.nowtime()
    screen_width, screen_height = sg.Window.get_screen_size()
    layout = [
    [sg.Text("Operator Initials:"), sg.Input(default_text="", key="operator", size=(20, 1))],
    [sg.Text("Time of Observation:"), sg.Input(default_text=default_time, key="timestamp", size=(20, 1))],
    [sg.Text("Time can be the hour (ex: 14) or in ISO time (ex: 2025-03-13T14:00) .",font=("Helvetica", 8, "italic"))],
    [sg.Text("Time will be round down to the closest hour.",font=("Helvetica", 8, "italic"))],
    
    [
        sg.Column([
            [sg.Text("North Basin (MGD)")],
            [sg.Text("  1:"), sg.Input(default_text="", key="north_basin_1_MGD", size=(5, 1))],
            [sg.Text("  3:"), sg.Input(default_text="", key="north_basin_3_MGD", size=(5, 1))],
            [sg.Text("  5:"), sg.Input(default_text="", key="north_basin_5_MGD", size=(5, 1))],
            [sg.Text("  7:"), sg.Input(default_text="", key="north_basin_7_MGD", size=(5, 1))],
            [sg.Text("  9:"), sg.Input(default_text="", key="north_basin_9_MGD", size=(5, 1))],
            [sg.Text("11:"), sg.Input(default_text="", key="north_basin_11_MGD", size=(5, 1))],
            [sg.Text("13:"), sg.Input(default_text="", key="north_basin_13_MGD", size=(5, 1))]
        ], justification='left',vertical_alignment='top'),
        sg.Column([     
            [sg.Text("South Basin (MGD)")],
            [sg.Text("  1:"), sg.Input(default_text="", key="south_basin_1_MGD", size=(5, 1))],
            [sg.Text("  3:"), sg.Input(default_text="", key="south_basin_3_MGD", size=(5, 1))],
            [sg.Text("  5:"), sg.Input(default_text="", key="south_basin_5_MGD", size=(5, 1))],
            [sg.Text("  7:"), sg.Input(default_text="", key="south_basin_7_MGD", size=(5, 1))],
            [sg.Text("  9:"), sg.Input(default_text="", key="south_basin_9_MGD", size=(5, 1))],
            [sg.Text("11:"), sg.Input(default_text="", key="south_basin_11_MGD", size=(5, 1))],
            [sg.Text("13:"), sg.Input(default_text="", key="south_basin_13_MGD", size=(5, 1))]
        ], justification='left',vertical_alignment='top'),
        sg.Column([
            [sg.Text("North Clarifier (MGD)")], 
            [sg.Text("1:"), sg.Input(default_text="", key="north_clarifier_1_MGD", size=(5, 1))],
            [sg.Text("2:"), sg.Input(default_text="", key="north_clarifier_2_MGD", size=(5, 1))],
            [sg.Text("3:"), sg.Input(default_text="", key="north_clarifier_3_MGD", size=(5, 1))],
            [sg.Text("4:"), sg.Input(default_text="", key="north_clarifier_4_MGD", size=(5, 1))]
        ], justification='left',vertical_alignment='top'),
        sg.Column([
            [sg.Text("South Clarifier (MGD)")],
            [sg.Text("1:"), sg.Input(default_text="", key="south_clarifier_1_MGD", size=(5, 1))],
            [sg.Text("2:"), sg.Input(default_text="", key="south_clarifier_2_MGD", size=(5, 1))],
            [sg.Text("3:"), sg.Input(default_text="", key="south_clarifier_3_MGD", size=(5, 1))],
            [sg.Text("4:"), sg.Input(default_text="", key="south_clarifier_4_MGD", size=(5, 1))]
        ], justification='left',vertical_alignment='top'),
        sg.Column([
            [sg.Text("North RAS (MGD)")],
            [sg.Text("1:"), sg.Input(default_text="", key="north_ras_1_MGD", size=(5, 1))],
            [sg.Text("2:"), sg.Input(default_text="", key="north_ras_2_MGD", size=(5, 1))],
            [sg.Text("3:"), sg.Input(default_text="", key="north_ras_3_MGD", size=(5, 1))],
            [sg.Text("4:"), sg.Input(default_text="", key="north_ras_4_MGD", size=(5, 1))]
        ], justification='left',vertical_alignment='top'),
        sg.Column([
            [sg.Text("South RAS (MGD)")],
            [sg.Text("1:"), sg.Input(default_text="", key="south_ras_1_MGD", size=(5, 1))],
            [sg.Text("2:"), sg.Input(default_text="", key="south_ras_2_MGD", size=(5, 1))],
            [sg.Text("3:"), sg.Input(default_text="", key="south_ras_3_MGD", size=(5, 1))],
            [sg.Text("4:"), sg.Input(default_text="", key="south_ras_4_MGD", size=(5, 1))]
        ], justification='left',vertical_alignment='top')
    ],
    [sg.Button("Submit"), sg.Button("Close")],
    [sg.Text("If you submit multiple values in an hour, the most recent one will be used.",font=("Helvetica", 8, "italic"))]
    ]

    window = sg.Window("Hourly Basins and Clarifiers Frame", layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Close":
            break
        if event == "Submit":
            try:
                # Sanitize and process input values
                data = {
                    "timestamp_entry_ISO": helpers.nowtime(),
                    "timestamp_intended_ISO": helpers.sanitize_time(values["timestamp"]),
                    "operator": values["operator"],
                    "source": "local-gui-Python-FreeSimpleGUI",
                    "north_basin_1_MGD": helpers.check_values_float(values["north_basin_1_MGD"]),
                    "north_basin_3_MGD": helpers.check_values_float(values["north_basin_3_MGD"]),
                    "north_basin_5_MGD": helpers.check_values_float(values["north_basin_5_MGD"]),
                    "north_basin_7_MGD": helpers.check_values_float(values["north_basin_7_MGD"]),
                    "north_basin_9_MGD": helpers.check_values_float(values["north_basin_9_MGD"]),
                    "north_basin_11_MGD": helpers.check_values_float(values["north_basin_11_MGD"]),
                    "north_basin_13_MGD": helpers.check_values_float(values["north_basin_13_MGD"]),

                    "south_basin_1_MGD": helpers.check_values_float(values["south_basin_1_MGD"]),
                    "south_basin_3_MGD": helpers.check_values_float(values["south_basin_3_MGD"]),
                    "south_basin_5_MGD": helpers.check_values_float(values["south_basin_5_MGD"]),
                    "south_basin_7_MGD": helpers.check_values_float(values["south_basin_7_MGD"]),
                    "south_basin_9_MGD": helpers.check_values_float(values["south_basin_9_MGD"]),
                    "south_basin_11_MGD": helpers.check_values_float(values["south_basin_11_MGD"]),
                    "south_basin_13_MGD": helpers.check_values_float(values["south_basin_13_MGD"]),

                    "north_clarifier_1_MGD": helpers.check_values_float(values["north_clarifier_1_MGD"]),
                    "north_clarifier_2_MGD": helpers.check_values_float(values["north_clarifier_2_MGD"]),
                    "north_clarifier_3_MGD": helpers.check_values_float(values["north_clarifier_3_MGD"]),
                    "north_clarifier_4_MGD": helpers.check_values_float(values["north_clarifier_4_MGD"]),

                    "south_clarifier_1_MGD": helpers.check_values_float(values["south_clarifier_1_MGD"]),
                    "south_clarifier_2_MGD": helpers.check_values_float(values["south_clarifier_2_MGD"]),
                    "south_clarifier_3_MGD": helpers.check_values_float(values["south_clarifier_3_MGD"]),
                    "south_clarifier_4_MGD": helpers.check_values_float(values["south_clarifier_4_MGD"]),

                    "north_ras_1_MGD": helpers.check_values_float(values["north_ras_1_MGD"]),
                    "north_ras_2_MGD": helpers.check_values_float(values["north_ras_2_MGD"]),
                    "north_ras_3_MGD": helpers.check_values_float(values["north_ras_3_MGD"]),
                    "north_ras_4_MGD": helpers.check_values_float(values["north_ras_4_MGD"]),

                    "south_ras_1_MGD": helpers.check_values_float(values["south_ras_1_MGD"]),
                    "south_ras_2_MGD": helpers.check_values_float(values["south_ras_2_MGD"]),
                    "south_ras_3_MGD": helpers.check_values_float(values["south_ras_3_MGD"]),
                    "south_ras_4_MGD": helpers.check_values_float(values["south_ras_4_MGD"])                 
                }
                
            except Exception as e:
                print(f"Error passing data: {e}")
                sg.PopupError(f"Failed to save data: {e}")
                data = None

            if data is not None:
                try:
                    response = requests.post("http://localhost:8000/submit-basin-clarifier-hourly", data=data)
                    print(f"Server response: {response.json()}")
                except Exception as e:
                    print(f"Error passing data: {e}")
                    print("Web app not running, defaulting to local export.")

                    helpers.local_save_data_basin_clarifier_hourly(data)
                    sg.Popup("Hourly data saved successfully!")
            
    window.close()

if __name__ == "__main__":
    hourly_basin_clarifiers_window()
