import FreeSimpleGUI as sg
import time

# Define the layout
layout = [
    [sg.Text("Running Command with Animation...")],
    [sg.Output(size=(50, 10), key='-OUTPUT-')],
    [sg.Button("Start"), sg.Button("Exit")]
]

# Create the window
window = sg.Window("Shell with Animation", layout)

while True:
    event, values = window.read(timeout=100)  # Non-blocking read
    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    if event == "Start":
        # Simulate a shell command with animation
        for i in range(10):
            print(f"Step {i + 1}/10: Processing...")
            time.sleep(0.5)  # Simulate processing time
            window.refresh()

window.close()
