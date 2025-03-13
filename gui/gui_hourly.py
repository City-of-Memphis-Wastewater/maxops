import requests
import FreeSimpleGUI as sg
import app.utils.helpers as helpers

def hourly_window():
    default_time = helpers.nowtime()
    layout = [
        [sg.Text("Operator Name:"), sg.InputText(default_text="Clayton Bennett", key="operator")],
        [sg.Text("Timestamp (ISO Format):"), sg.InputText(default_text=default_time, key="timestamp")],
        [sg.Text("Influent Flow Rate (MGD):"), sg.InputText(default_text="0.0", key="influent_flow_rate_MGD")],
        [sg.Text("After Wet Well Flow Rate (MGD):"), sg.InputText(default_text="0.0", key="after_wet_well_flow_rate_MGD")],
        [sg.Text("Effluent Flow Rate (MGD):"), sg.InputText(default_text="0.0", key="effluent_flow_rate_MGD")],
        [sg.Text("WAS Flow Rate (MGD):"), sg.InputText(default_text="0.0", key="was_flow_rate_MGD")],
        [sg.Text("COD Pre-Disinfection (mg/Liter):"),sg.InputText(default_text="0.0", key="cod_predisinfection_mgPerLiter")],
        [sg.Button("Submit"), sg.Button("Close")]
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
                    "influent_flow_rate_MGD": float(values["influent_flow_rate_MGD"]),
                    "after_wet_well_flow_rate_MGD": float(values["after_wet_well_flow_rate_MGD"]),
                    "effluent_flow_rate_MGD": float(values["effluent_flow_rate_MGD"]),
                    "was_flow_rate_MGD": float(values["was_flow_rate_MGD"]),
                    "cod_predisinfection_mgPerLiter": float(values["cod_predisinfection_mgPerLiter"]),
                    "operator": values["operator"],
                    "source": "local-gui-Python-FreeSimpleGUI"
                }
                
            except Exception as e:
                print(f"Error saving hourly data: {e}")
                sg.PopupError(f"Failed to save data: {e}")
                data = None

            if data is not None:
                try:
                    response = requests.post("http://localhost:8000/submit-hourly", data=data)
                    print(f"Server response: {response.json()}")
                except Exception as e:
                    print(f"Error spoofing hourly data: {e}")
                    print("Web app not running, defaulting to local export.")

                    helpers.local_save_data_hourly(data)
                    sg.Popup("Hourly data saved successfully!")
            
    window.close()

if __name__ == "__main__":
    hourly_window()
