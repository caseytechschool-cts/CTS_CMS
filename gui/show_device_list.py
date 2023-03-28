import os.path
from firebase.CURD import device_list, add_device_to_database
import PySimpleGUI as sg
from helper_lib.base64image import image_to_base64
from helper_lib.search import search_devices
from os import path
from pathlib import Path
import uuid
import csv
from menu import login_menu
from main import show_main_screen
from csv_files import csv_reader

table_heading = ['Device ID', 'Borrowed by', 'Device sub type', 'Device type', 'Faulty?', 'Device name']
font_underline = ('Century Gothic', 10, 'underline')
font_normal = ('Century Gothic', 10, '')

def show_device_list_window():
    sg.theme('Material1')
    table_data, status = device_list()
    filter_table_data = table_data
    layout_all_devices = [
        [sg.Menu(login_menu(), key='-menu-', background_color='white')],
        [sg.Push(), sg.ButtonMenu('Download', menu_def=['Download', ['Download all::-download-all-', 'Download selected::-download-selected-']],
                                  key='-download-device-list-', background_color='white'),
         sg.Input(default_text='Type here...', key='-filter-query-', do_not_clear=False),
         sg.Button(button_text='Filter', key='-filter-submit-button-'), sg.Push()],
        [sg.Table(values=table_data, headings=table_heading, key='-all-devices-', justification='center',
                  alternating_row_color='#b5c1ca', expand_x=True, expand_y=True, row_height=20, enable_events=True,
                  auto_size_columns=True, vertical_scroll_only=False)],
        [sg.Sizegrip()]
    ]

    max_width, max_height = sg.Window.get_screen_size()
    max_width = int(max_width*0.8)
    max_height = int(max_height*0.6)
    window_all_devices = sg.Window(title="CTS CMS",
                                   layout=layout_all_devices,
                                   size=(max_width, max_height),
                                   icon=image_to_base64('logo.png'),
                                   finalize=True,
                                   resizable=True)

    window_all_devices['-filter-query-'].bind('<Return>', '_Enter')
    while True:
        event, values = window_all_devices.read()
        print(event)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == '-download-device-list-':
            file_id = str(uuid.uuid4())
            if '-download-all-' in values[event]:
                file_name = f'All devices_{file_id}.csv'
            elif '-download-selected-' in values[event]:
                file_name = f'Selected devices_{file_id}.csv'

            download_path = path.join(Path.home(), 'Downloads', file_name)
            with open(download_path, 'w', newline="") as file:
                writer = csv.writer(file)
                writer.writerow(table_heading)
                if '-download-all-' in values[event]:
                    writer.writerows(table_data)
                elif '-download-selected-' in values[event]:
                    writer.writerows(filter_table_data)
                sg.popup_notify('Download completed! Check your Downloads folder.')
        if '-all-devices-' in event:
            selected_device = filter_table_data[values['-all-devices-'][0]]
            print(selected_device)
        if event == '-filter-submit-button-' or event == '-filter-query-' + '_Enter':
            print(values['-filter-query-'])
            query = values['-filter-query-']
            filter_table_data = search_devices(table_data, query)
            window_all_devices['-all-devices-'].update(values=filter_table_data)
        if event == 'Logout':
            window_all_devices.close()
            if path.exists(path.join('../security', 'auth.json')):
                os.remove(path.join('../security', 'auth.json'))
            show_main_screen()
        if event == 'Student QR code':
            csv_file_path = sg.popup_get_file(message='Upload student booking csv file', title='File uploader',
                                              font=font_normal, keep_on_top=True, file_types=(('CSV Files', '*.csv'),))
            # print(csv_file_path)
            csv_reader.csv_student_reader(filename=csv_file_path, default=False)
            sg.popup_notify('QRcode generation done! Check your Downloads folder.')
        if event == 'Devices':
            csv_file_path = sg.popup_get_file(message='Upload device csv file', title='File uploader',
                                              font=font_normal, keep_on_top=True, file_types=(('CSV Files', '*.csv'),))
            # print(csv_file_path)
            add_device_to_database(filename=csv_file_path, default=False)
            sg.popup_notify('Devices added successfully\n QRcode generation done! Check your Downloads folder.')



if __name__ == '__main__':
    show_device_list_window()
