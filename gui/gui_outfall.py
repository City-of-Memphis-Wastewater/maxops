import requests
import FreeSimpleGUI as sg
import app.utils.helpers as helpers

def outfall_window():
    default_time = helpers.nowtime()
    '''layout = [
        [sg.Text("Operator Name:"), sg.InputText(default_text="Clayton Bennett", key="operator")],
        [sg.Text("Time of Observation:"), sg.InputText(default_text=default_time, key="timestamp")],
        [sg.Text("Safe to Make Observation:"), sg.Checkbox("Yes", default=True, key="safe_to_make_observation")],
        [sg.Text("Floatable Present:"), sg.Checkbox("Yes", default=True, key="floatable_present")],
        [sg.Text("Scum Present:"), sg.Checkbox("Yes", default=False, key="scum_present")],
        [sg.Text("Foam Present:"), sg.Checkbox("Yes", default=False, key="foam_present")],
        [sg.Text("Oil Present:"), sg.Checkbox("Yes", default=True, key="oil_present")],
        [sg.Button("Submit"), sg.Button("Close")]
    ]'''
    layout = [
        [sg.Text("Operator Name:"), sg.InputText(default_text="Clayton Bennett", key="operator")],
        [sg.Text("Time of Observation:"), sg.InputText(default_text=default_time, key="timestamp")],
        [sg.Text("Safe to Make Observation:"), sg.Combo(["","Yes", "No"], default_value="", key="safe_to_make_observation")],
        [sg.Text("Floatable Present:"), sg.Combo(["","Yes", "No"], default_value="", key="floatable_present")],
        [sg.Text("Scum Present:"), sg.Combo(["","Yes", "No"], default_value="", key="scum_present")],
        [sg.Text("Foam Present:"), sg.Combo(["","Yes", "No"], default_value="", key="foam_present")],
        [sg.Text("Oil Present:"), sg.Combo(["","Yes", "No"], default_value="", key="oil_present")],
        [sg.Button("Submit"), sg.Button("Close")]
    ]

    window = sg.Window("Outfall Frame", layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Close":
            break
        if event == "Submit":
            print(values)  # For debugging or processing inputs
            # Validation check
            if any(values[key] == "" for key in ["safe_to_make_observation", "floatable_present", "scum_present", "foam_present", "oil_present"]):
                sg.popup("Please make a selection for all dropdown fields.")
            else:
                # Handle form submission
                print("Form submitted with values:", values)
            
                try:
                    # if you chanage these keys and the order, and a relevant CSV file already exists, you should see: "WARNING: The existing CSV column names DO NOT match data.keys()"
                    data = {
                        "timestamp_entry_ISO": helpers.nowtime(),
                        "timestamp_intended_ISO": helpers.sanitize_time(values["timestamp"]),
                        "safe_to_make_observation": values["safe_to_make_observation"],
                        "floatable_present": values["floatable_present"],
                        "scum_present": values["scum_present"],
                        "foam_present": values["foam_present"],
                        "oil_present": values["oil_present"],
                        "operator": values["operator"],
                        "source": "local-gui-Python-FreeSimpleGUI"
                    }

                except Exception as e:
                    print(f"Error spoofing hourly data: {e}")
                    data = None
                    sg.PopupError(f"Failed to save data: {e}")

                if data is not None:
                    try:
                        response = requests.post("http://localhost:8000/submit-outfall", data=data)
                        print(f"Server response: {response.json()}")
                    except Exception as e:
                        print(f"Error spoofing daily data: {e}")
                        print("Web app not running, defaulting to local export.")

                        helpers.local_save_data_outfall(data)
                        sg.Popup("Data saved successfully!")
    window.close()

if __name__ == "__main__":
    outfall_window()