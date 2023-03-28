import PySimpleGUI as sg
from helper_lib.pathmaker import resource_path
import time
import threading


def download_files():
    # Download files here
    time.sleep(5)  # simulate file download process


def main():
    layout = [
        [sg.Image(filename=resource_path('../assets/splash.gif'), background_color='white', key='-IMAGE-')],
        [sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],
        [sg.StatusBar('This is the statusbar')]
    ]

    window = sg.Window('CTS CMS', layout, no_titlebar=True, keep_on_top=True, size=(500, 300), element_padding=(0, 0),
                       finalize=True)
    window['-EXPAND-'].expand(True, True, True)


    # Create a thread for downloading files
    thread = threading.Thread(target=download_files)
    thread.start()

    # Loop until the GUI window is closed
    while True:
        event, values = window.read(timeout=100)

        # If the thread has finished downloading files, close the splash screen
        if not thread.is_alive():
            window.close()
            break

        # Update the splash screen image
        if event == sg.TIMEOUT_EVENT:
            window['-IMAGE-'].update_animation(resource_path('../assets/splash.gif'), time_between_frames=100)

        # Check if the user wants to close the window
        if event == sg.WIN_CLOSED:
            break


if __name__ == '__main__':
    main()
