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

import FreeSimpleGUI as sg
from gui.gui_outfall import outfall_window
from gui.gui_hourly import hourly_window
import os
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
        [sg.Button("Hourly", key="-HOURLY-"), sg.Button("Hourly History", key="-HOURLY-KNOWN-")], 
        [sg.Button("Exit", key="-EXIT-")]
    ]
    window = sg.Window("Main Menu", layout)

    while True:
        event, _ = window.read()
        if event == sg.WINDOW_CLOSED or event == "-EXIT-":
            break
        if event == "-OUTFALL-":
            outfall_window()
        if event == "-HOURLY-":
            hourly_window()
        if event == "-OUTFALL-KNOWN-":
            json_file = os.path.join("exports","intermediate" ,"outfall_daily_data.json")
            layout_title = "Daily Outfall Data Submissions"
            window_label = "Outfall Data Viewer"
            known_window(json_file, layout_title, window_label)
        if event == "-HOURLY-KNOWN-":
            json_file = os.path.join("exports","intermediate" ,"hourly_data.json")
            layout_title = "Hourly Data Submissions"
            window_label = "Hourly Data Viewer"
            known_window(json_file, layout_title, window_label)

    window.close()

if __name__ == "__main__":
    menu_window()
