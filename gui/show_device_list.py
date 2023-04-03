import os.path
from firebase.CURD import device_list, add_device_to_database, remove_device_from_database
from firebase.config import *
import PySimpleGUI as sg
from helper_lib.base64image import image_to_base64
from helper_lib.search import search_devices
from thread_functions import save_device_list
from os import path
from pathlib import Path
import uuid
from menu import login_menu
from main import show_main_screen
from csv_files import csv_reader
from threading import Thread
from schedule import repeat,every,run_pending
import json
from device_modifier import modify_device
from device_report import report_device


# def stream_handler(message):
#     data = []
#     print(message["event"]) # put
#     print(message["path"]) # /-K7yGTTEp7O549EzTYtI
#     # print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
#     print(type(message['data']))
#     # for key, value in message['data'].items():
#     #     data.append(value)
#     # print(data)
#
#
# my_stream = db.child("devices").stream(stream_handler)

table_heading = ['Device ID', 'Device sub type', 'Device type', 'Faulty?', 'Location', 'Device name']
col_map = [False, True, True, True, True, True]
font_underline = ('Century Gothic', 10, 'underline')
font_normal = ('Century Gothic', 10, '')
user = None


@repeat(every(1).hour)
def refresh_token(user_auth):
    global user
    user = auth.refresh(user_auth['refreshToken'])
    with open(os.path.join('../security', "auth.json"), "w") as outfile:
        json.dump(user, outfile)


def show_device_list_window(user_auth):
    sg.theme('Material1')
    if user is None:
        idToken = user_auth['idToken']
    else:
        idToken = user['idToken']
    table_data, status = device_list(idToken)
    filter_table_data = table_data
    header_padding = ((5, 5), (20, 20))
    layout_all_devices = [
        [sg.Menu(login_menu(), key='-menu-', background_color='white')],
        [sg.Push(), sg.ButtonMenu('  Download  ', menu_def=['Download', ['Download all::-download-all-',
                                                                     'Download selected::-download-selected-']],
                                  key='-download-device-list-', background_color='white', pad=header_padding),
         sg.Input(default_text='Type here...', key='-filter-query-', do_not_clear=False, pad=header_padding),
         sg.Button(button_text='  Filter  ', key='-filter-submit-button-', pad=header_padding),
         sg.Button(button_text='  Modify  ', key='-modify-device-button-', visible=False, button_color='#2db52c',
                   pad=header_padding),
         sg.Button(button_text='  Report as faulty  ', key='-faulty-report-device-button-', visible=False, button_color='#fcb116', pad=header_padding),
         sg.Button(button_text='  Delete  ', key='-delete-device-button-', visible=False, button_color='#de5260', pad=header_padding),
        sg.Button(button_text='   Fault details   ', pad=header_padding, key='-fault-details-', visible=False, button_color='#ff696a'),
         sg.Button(button_text='  Mark as resolved  ', pad=header_padding, key='-mark-as-resolved-', visible=False, button_color='#2db52c'), sg.Push()],
        [sg.Table(values=table_data, headings=table_heading, key='-all-devices-', justification='center',
                  alternating_row_color='#b5c1ca', expand_x=True, expand_y=True, row_height=20, enable_events=True,
                  auto_size_columns=True, vertical_scroll_only=False, visible_column_map=col_map)],
        [sg.Sizegrip()]
    ]

    max_width, max_height = sg.Window.get_screen_size()
    max_width = int(max_width * 0.8)
    max_height = int(max_height * 0.6)
    window_all_devices = sg.Window(title="CTS CMS",
                                   layout=layout_all_devices,
                                   size=(max_width, max_height),
                                   icon=image_to_base64('logo.png'),
                                   finalize=True,
                                   resizable=True)

    window_all_devices['-filter-query-'].bind('<Return>', '_Enter')

    thread_device_upload = None
    thread_student_qrcode = None
    thread_download_csv = None

    while True:
        event, values = window_all_devices.read()
        run_pending()
        print(event)
        if event == '-Thread-device-upload-':
            sg.popup_notify('Devices added successfully\nQRcode generation done! Check your Downloads folder.')
        if event == '-Thread-csv-download-':
            sg.popup_notify('Download completed! Check your Downloads folder.')
        if event == '-Thread-student-qrcode-':
            sg.popup_notify('QRcode generation completed! Check your Downloads folder.')
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == '-delete-device-button-':
            result = sg.popup_ok_cancel('Are you sure you want to delete this device? This action will remove it completely.',
                                        title='Delete device', font=font_normal, icon=image_to_base64('logo.png'))
            if result == 'OK':
                remove_device_from_database(selected_device[0], idToken)
                sg.popup_notify('Device deleted successfully.')
        if event == '-download-device-list-':
            file_id = str(uuid.uuid4())
            if '-download-all-' in values[event]:
                file_name = f'All devices_{file_id}.csv'
                download_path = path.join(Path.home(), 'Downloads', file_name)
                thread_download_csv = Thread(target=save_device_list.save,
                                             args=(download_path, table_heading, table_data, window_all_devices))
                thread_download_csv.start()
            elif '-download-selected-' in values[event]:
                file_name = f'Selected devices_{file_id}.csv'
                download_path = path.join(Path.home(), 'Downloads', file_name)
                thread_download_csv = Thread(target=save_device_list.save,
                                             args=(download_path, table_heading, filter_table_data, window_all_devices))
                thread_download_csv.start()
        if '-all-devices-' in event:
            selected_device = filter_table_data[values['-all-devices-'][0]]
            window_all_devices['-modify-device-button-'].update(visible=True)
            window_all_devices['-faulty-report-device-button-'].update(visible=True)
            window_all_devices['-delete-device-button-'].update(visible=True)
            window_all_devices['-fault-details-'].update(visible=selected_device[3])
            window_all_devices['-mark-as-resolved-'].update(visible=selected_device[3])
        if event == '-modify-device-button-':
            modify_device(selected_device, idToken)
        if event == '-faulty-report-device-button-':
            report_device(selected_device, idToken)
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
                                              font=font_normal, keep_on_top=True, file_types=(('CSV Files', '*.csv'),),
                                              icon=image_to_base64('logo.png'))
            if csv_file_path:
                thread_student_qrcode = Thread(target=csv_reader.csv_student_reader,
                                               args=(window_all_devices, csv_file_path, False))
                thread_student_qrcode.start()
        if event == 'Devices':
            csv_file_path = sg.popup_get_file(message='Upload device csv file', title='File uploader',
                                              font=font_normal, keep_on_top=True, file_types=(('CSV Files', '*.csv'),),
                                              icon=image_to_base64('logo.png'))
            if csv_file_path:
                thread_device_upload = Thread(target=add_device_to_database,
                                              args=(window_all_devices, csv_file_path, idToken, False))
                thread_device_upload.start()

    if thread_device_upload is not None:
        thread_device_upload.join()
    if thread_download_csv is not None:
        thread_download_csv.join()
    if thread_student_qrcode is not None:
        thread_student_qrcode.join()
    window_all_devices.close()


if __name__ == '__main__':
    show_device_list_window()

