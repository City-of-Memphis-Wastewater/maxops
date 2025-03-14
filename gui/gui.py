'''
[Title]:
gui.py
[Author] 
"Clayton Bennett"
[Created] 
date(08 March 2025)

[[Description]]
"""freesimplegui implementation for wateropforms;
try: pip install poetry

run this installation command:
poetry add wateropforms # in powershell, bash, termux, and on. ;
write this python script: #README.md
from wateropforms import wateropforms as wof
print(f"dir(wof) = {dir(wof)}")
"""
[[Purpose]]
"mock up the appearance of the data entry"

'''
import os
import FreeSimpleGUI as sg

from gui.gui_outfall import outfall_window
from gui.gui_hourly import overview_hourly_window
from gui.gui_basins_clarifiers_hourly import hourly_basin_clarifiers_window
from gui.gui_known import known_window

#print(dir(sg))
#sg.user_settings_object
#sg.ttk
#sg.warnings

def do_browsefiles(args):
    file_path = sg.popup_get_file("Select a filepath to assign to variable!")
    return file_path

def menu_window():
    layout = [
        [sg.Button("Outfall", key="-OUTFALL-"), sg.Button("Outfall History", key="-OUTFALL-KNOWN-")],
        [sg.Button("Overview Hourly", key="-OVERVIEW-HOURLY-"), sg.Button("Hourly History of Overview Numbers", key="-HOURLY-KNOWN-")], 
        [sg.Button("Hourly Basins and Clarifiers", key="-BASINS-CLARIFIERS-"), sg.Button("Hourly Basins Clarifers History", key="-BASINS-CLARIFIERS-KNOWN-")], 
        [sg.Button("Exit", key="-EXIT-")]
    ]
    window = sg.Window("MaxOps Menu", layout)

    while True:
        event, _ = window.read()
        if event == sg.WINDOW_CLOSED or event == "-EXIT-":
            break
        if event == "-OUTFALL-":
            outfall_window()
        if event == "-OVERVIEW-HOURLY-":
            overview_hourly_window()
        if event == "-BASINS-CLARIFIERS-":
            hourly_basin_clarifiers_window()
        if event == "-OUTFALL-KNOWN-":
            json_file = os.path.join("exports","intermediate" ,"outfall_daily_data.json")
            layout_title = "Daily Outfall Data Submissions"
            window_label = "Outfall Data Viewer"
            try:
                known_window(json_file, layout_title, window_label)
            except Exception as e:
                print(f"Error launching {window_label} data: {e}")

        if event == "-HOURLY-KNOWN-":
            json_file = os.path.join("exports","intermediate" ,"flows_and_cod_hourly_data.json")
            layout_title = "Hourly Data Submissions"
            window_label = "Hourly Data Viewer"
            try:
                known_window(json_file, layout_title, window_label)
            except Exception as e:
                print(f"Error launching {window_label} data: {e}")

        if event == "-BASINS-CLARIFIERS-KNOWN-":
            json_file = os.path.join("exports","intermediate" ,"basin_clarifier_hourly_data.json")
            layout_title = "Hourly Basin and Clarifier Data Submissions"
            window_label = "Hourly Basin and Clarifier Data Viewer"
            try:
                known_window(json_file, layout_title, window_label)
            except Exception as e:
                print(f"Error launching {window_label} data: {e}")

    window.close()

if __name__ == "__main__":
    menu_window()
