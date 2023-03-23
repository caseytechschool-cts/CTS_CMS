from firebase.CURD import device_list
import PySimpleGUI as sg
from helper_lib.base64image import image_to_base64
from os import path
from pathlib import Path
import uuid
import csv

table_heading = ['Borrowed by', 'Device sub type', 'Device type', 'Faulty?', 'Device name']
right_click_table_menu = ['', ['Update', 'Report as faulty', '---', 'Delete']]
button_menu = ['', ['Borrowed by', 'Sub type', 'Type', 'Name']]


def show_device_list_window():
    table_data, status = device_list()
    layout_all_devices = [
        [sg.Push(), sg.Button('Download device list', key='-download-device-list-'),
         sg.Input(default_text='Type here...', key='-filter-query-', do_not_clear=False),
         sg.Button(button_text='Filter', key='-filter-submit-button-'), sg.Push()],
        [sg.Table(values=table_data, headings=table_heading, key='-all-devices-', justification='center',
                  alternating_row_color='#b5c1ca', expand_x=True, expand_y=True, visible=True,
                  display_row_numbers=True, row_height=20, enable_events=True, right_click_menu=right_click_table_menu,
                  select_mode=sg.TABLE_SELECT_MODE_NONE)],
    ]

    window_all_devices = sg.Window(title="Device list",
                                   layout=layout_all_devices,
                                   size=(800, 600),
                                   icon=image_to_base64('logo.png'),
                                   finalize=True)

    window_all_devices['-filter-query-'].bind('<Return>', '_Enter')
    while True:
        event, values = window_all_devices.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        print(event)
        if event == '-download-device-list-':
            file_id = str(uuid.uuid4())
            file_name = f'All devices_{file_id}.csv'
            download_path = path.join(Path.home(), 'Downloads', file_name)
            with open(download_path, 'w', newline="") as file:
                writer = csv.writer(file)
                writer.writerow(table_heading)
                writer.writerows(table_data)
                sg.popup_notify('Download completed! Check your Downloads folder.')
        if '-all-devices-' in event:
            selected_device = table_data[values['-all-devices-'][0]]
        if event == '-filter-submit-button-' or event == '-filter-query-'+'_Enter':
            print(values['-filter-query-'])
            query = values['-filter-query-']
            filter_table_data = list(filter(lambda device: query.lower() in device[-1].lower(), table_data))
            window_all_devices['-all-devices-'].update(values=filter_table_data)
            # window_all_devices.refresh()

