import requests
import FreeSimpleGUI as sg
import app.utils.helpers as helpers

def hourly_window():
    default_time = helpers.nowtime()
    layout = [
        [sg.Text("Operator Initials:"), sg.InputText(default_text="", key="operator", size=(20, 1))],
        [sg.Text("Time of Observation:"), sg.InputText(default_text=default_time, key="timestamp", size=(20, 1))],
        [sg.Text("Time can be the hour (ex: 14) or in ISO time (ex: 2025-03-13T14:00) .",font=("Helvetica", 8, "italic"))],
        [sg.Text("Time will be round down to the closest hour.",font=("Helvetica", 8, "italic"))],
        [sg.Text("Influent Flow Rate (MGD):"), sg.InputText(default_text="", key="influent_flow_rate_MGD", size=(9, 1))],
        [sg.Text("After Wet Well Flow Rate (MGD):"), sg.InputText(default_text="", key="after_wet_well_flow_rate_MGD", size=(9, 1))],
        [sg.Text("Effluent Flow Rate (MGD):"), sg.InputText(default_text="", key="effluent_flow_rate_MGD", size=(9, 1))],
        [sg.Text("WAS Flow Rate (MGD):"), sg.InputText(default_text="", key="was_flow_rate_MGD", size=(9, 1))],
        [sg.Text("COD Pre-Disinfection (mg/Liter):"),sg.InputText(default_text="", key="cod_predisinfection_mgPerLiter", size=(9, 1))],
        [sg.Button("Submit"), sg.Button("Close")],
        [sg.Text("If you submit multiple values in an hour, the most recent one will be used.",font=("Helvetica", 8, "italic"))]
    ]

    window = sg.Window("Hourly Frame", layout)

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
                    "influent_flow_rate_MGD": helpers.check_values_float(values["influent_flow_rate_MGD"]),
                    "after_wet_well_flow_rate_MGD": helpers.check_values_float(values["after_wet_well_flow_rate_MGD"]),
                    "effluent_flow_rate_MGD": helpers.check_values_float(values["effluent_flow_rate_MGD"]),
                    "was_flow_rate_MGD": helpers.check_values_float(values["was_flow_rate_MGD"]),
                    "cod_predisinfection_mgPerLiter": helpers.check_values_float(values["cod_predisinfection_mgPerLiter"])                    
                }
                
            except Exception as e:
                print(f"Error passing data: {e}")
                sg.PopupError(f"Failed to save data: {e}")
                data = None

            if data is not None:
                try:
                    response = requests.post("http://localhost:8000/submit-hourly", data=data)
                    print(f"Server response: {response.json()}")
                except Exception as e:
                    print(f"Error passing data: {e}")
                    print("Web app not running, defaulting to local export.")

                    helpers.local_save_data_hourly(data)
                    sg.Popup("Hourly data saved successfully!")
            
    window.close()

if __name__ == "__main__":
    hourly_window()
