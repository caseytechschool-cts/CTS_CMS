# https://www.cos.net.au/office-products/labels/Printec-General-Use-Labels-24-Per-Sheet-LABL5420
import csv
import os.path
from firebase.CURD import add_device_to_database, remove_device_from_database
from firebase.config import *
import PySimpleGUI as sg
from helper_lib.base64image import image_to_base64
from helper_lib.pathmaker import resource_path
from helper_lib.search import search_devices
from thread_functions import save_device_list
import uuid
from gui.menu import login_menu
from main import show_main_screen
from threading import Thread
from schedule import repeat, every, run_pending
import json
from gui.device_modifier import modify_device
from gui.device_report import report_device
from gui.fault_details_window import fault_details
from . import student_name_tag_window
from . import device_tag_window
from . import borrower_list_window
from constant.global_info import *
import webbrowser

table_data = []
filter_table_data = []
window_all_devices = None
my_stream = None


def create_json_file(csv_files):
    students = {}
    csv_files_path = csv_files.split(';')
    for filepath in csv_files_path:
        with open(filepath) as file:
            csv_data = csv.reader(file)
            line_count = 0
            for row in csv_data:
                if line_count:
                    student = [
                        row[1] + ' ' + row[2],
                        row[3],
                        row[4]
                    ]
                    students[row[5]] = student
                else:
                    line_count += 1

    # print(students)
    with open(path.join(user_data_location, 'booking.json'), 'w') as fp:
        json.dump(students, fp)


def update_device(device_id, device_updated_data):
    change_main_table = False
    change_filterred_table = False
    for index in range(len(table_data)):
        if table_data[index][0] == device_id:
            for key, val in device_updated_data.items():
                if key == 'device_sub_type':
                    table_data[index][1] = val
                if key == 'device_type':
                    table_data[index][2] = val
                if key == 'isFaulty':
                    table_data[index][3] = val
                if key == 'location':
                    table_data[index][4] = val
                if key == 'name':
                    table_data[index][5] = val
                if key == 'purpose':
                    table_data[index][6] = val
            change_main_table = True
            break
    if change_main_table:
        window_all_devices.write_event_value('-table-item-update-', 'full-table')

    for index in range(len(filter_table_data)):
        if filter_table_data[index][0] == device_id:
            for key, val in device_updated_data.items():
                if key == 'device_sub_type':
                    filter_table_data[index][1] = val
                if key == 'device_type':
                    filter_table_data[index][2] = val
                if key == 'isFaulty':
                    filter_table_data[index][3] = val
                if key == 'location':
                    filter_table_data[index][4] = val
                if key == 'name':
                    filter_table_data[index][5] = val
                if key == 'purpose':
                    table_data[index][6] = val
            change_filterred_table = True
            break
    if change_filterred_table:
        window_all_devices.write_event_value('-table-item-update-', 'filter-table')


def get_device_list_from_stream(device_list):
    global filter_table_data, table_data
    for key, val in device_list.items():
        entry = [key]
        for key1, val1 in val.items():
            entry.append(val1)
        table_data.append(entry)

    filter_table_data = table_data
    window_all_devices.write_event_value('-table-item-added-', 'full-table')


def add_device_to_table_data(device_id, row_data):
    row_data_to_add = [device_id]
    for item_key, item_val in row_data.items():
        row_data_to_add.append(item_val)
    table_data.append(row_data_to_add)
    # filter_table_data.append(row_data_to_add)
    window_all_devices.write_event_value('-table-item-added-', 'full-table')


def delete_item_from_table(device_id):
    change_main_table = False
    change_filterred_table = False
    for index in range(len(table_data)):
        if table_data[index][0] == device_id:
            del table_data[index]
            change_main_table = True
            break
    if change_main_table:
        window_all_devices.write_event_value('-table-item-delete-', 'full-table')

    for index in range(len(filter_table_data)):
        if filter_table_data[index][0] == device_id:
            del filter_table_data[index]
            change_filterred_table = True
            break
    if change_filterred_table:
        window_all_devices.write_event_value('-table-item-delete-', 'filter-table')


def stream_handler(message):
    # print(message['event'], message['data'], message['path'])
    # print('helo from func')
    if message['event'] == 'put' and isinstance(message['data'], type(None)) and message['path'] != '/':
        document_id = message['path'][1:]
        delete_item_from_table(document_id)
    elif message['event'] == 'put' and isinstance(message['data'], type(None)) and message['path'] == '/':
        global table_data, filter_table_data
        table_data = []
        filter_table_data = []
        window_all_devices.write_event_value('-table-delete-', 'all')
    elif message['event'] == 'patch' and isinstance(message['data'], dict):
        update_device(message['path'][1:], message['data'])
    elif message['event'] == 'put' and isinstance(message['data'], dict) and message['path'] != '/':
        add_device_to_table_data(message['path'][1:], message['data'])
    elif message['event'] == 'put' and isinstance(message['data'], dict):
        get_device_list_from_stream(message['data'])


table_heading = ['Device ID', 'Device sub type', 'Device type', 'Faulty?', 'Location', 'Device name', 'Purpose']
col_map = [False, True, True, True, True, True, True]
user = None


# @repeat(every(1).hour)
# def refresh_token(user_auth):
#     global user
#     user = auth.refresh(user_auth['refreshToken'])
#     with open(os.path.join(user_data_location, "auth.json"), "w") as outfile:
#         json.dump(user, outfile)


def show_device_list_window(user_auth):
    sg.theme('Material1')
    show_main_table = True
    if user is None:
        idToken = user_auth['idToken']
    else:
        idToken = user['idToken']
    global table_data, filter_table_data, my_stream
    my_stream = db.child("devices").stream(stream_handler, token=idToken)
    header_padding = ((5, 5), (20, 20))
    layout_all_devices = [
        [sg.Menu(login_menu(), key='-menu-', background_color='white')],
        [sg.Push(), sg.ButtonMenu('Download', menu_def=['Download', ['Download all::-download-all-',
                                                                         'Download selected::-download-selected-']],
                                  key='-download-device-list-', background_color='white', pad=header_padding,
                                  font=font_normal, size=(len('Download')+5, 1)),
         sg.Input(default_text='', key='-filter-query-', do_not_clear=True, pad=header_padding, font=font_normal),
         sg.Button(button_text='Filter', key='-filter-submit-button-', pad=header_padding, font=font_normal,
                   size=(len('Filter')+5, 1)),
         sg.Button(button_text='Modify', key='-modify-device-button-', visible=False, button_color='#2db52c',
                   pad=header_padding, font=font_normal, size=(len('Modify')+5, 1)),
         sg.Button(button_text='Report as faulty', key='-faulty-report-device-button-', visible=False,
                   button_color='#fcb116', pad=header_padding, font=font_normal, size=(len('Report as faulty')+5, 1)),
         sg.Button(button_text='Delete', key='-delete-device-button-', visible=False, button_color='#de5260',
                   pad=header_padding, font=font_normal, size=(len('Delete')+5, 1)),
         sg.Button(button_text='Fault details', pad=header_padding, key='-fault-details-', visible=False,
                   button_color='#ff696a', font=font_normal, size=(len('Fault details')+5, 1)),
         sg.Button(button_text='Mark as resolved', pad=header_padding, key='-mark-as-resolved-', visible=False,
                   button_color='#2db52c', font=font_normal, size=(len('Mark as resolved')+5, 1)), sg.Push()],
        [sg.Table(values=table_data, headings=table_heading, key='-all-devices-', justification='center',
                  alternating_row_color='#b5c1ca', expand_x=True, expand_y=True, row_height=20, enable_events=True,
                  auto_size_columns=True, vertical_scroll_only=False, visible_column_map=col_map,
                  display_row_numbers=True, font=font_normal,
                  select_mode=sg.TABLE_SELECT_MODE_BROWSE)],
        [sg.Sizegrip()]
    ]

    max_width, max_height = sg.Window.get_screen_size()
    max_width = int(max_width * 0.8)
    max_height = int(max_height * 0.6)
    global window_all_devices
    window_all_devices = sg.Window(title="CTS CMS :: Device list",
                                   layout=layout_all_devices,
                                   size=(max_width, max_height),
                                   icon=image_to_base64(resource_path(path.join('assets', 'logo.png'))),
                                   finalize=True,
                                   resizable=True,
                                   font=font_normal)

    window_all_devices['-filter-query-'].bind('<Return>', '_Enter')

    thread_device_upload = None
    thread_student_qrcode = None
    thread_download_csv = None

    while True:
        event, values = window_all_devices.read(timeout=100)
        # print(event)
        # run_pending()
        if event == 'Documentation':
            webbrowser.open_new_tab('https://casey-tech-school.gitbook.io/cts_cms/')
        if event == '-Thread-device-upload-':
            sg.popup_quick_message('Devices added successfully.', font=font_normal)
            result = sg.popup_ok_cancel('Do you want to generate device QR Code?',
                                        title='Device QR Code', font=font_normal,
                                        icon=image_to_base64(resource_path(path.join('assets', 'logo.png'))))
            if result == 'OK':
                device_tag_window.device_tag(csv_files=csv_file_path)
        if event == '-Thread-csv-download-':
            sg.popup_quick_message('Download completed! Check your Downloads folder.', auto_close_duration=1,
                                   font=font_normal)
        if event == '-Thread-student-qrcode-':
            sg.popup_quick_message('QRcode generation completed! Check your Downloads folder.', auto_close_duration=1,
                                   font=font_normal)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == '-delete-device-button-':
            result = sg.popup_ok_cancel(
                'Are you sure you want to delete this device? This action will remove it completely.',
                title='Delete device', font=font_normal,
                icon=image_to_base64(resource_path(path.join('assets', 'logo.png'))))
            if result == 'OK':
                remove_device_from_database(selected_device[0], idToken)
                window_all_devices['-modify-device-button-'].update(visible=False)
                window_all_devices['-faulty-report-device-button-'].update(visible=False)
                window_all_devices['-delete-device-button-'].update(visible=False)
                window_all_devices['-fault-details-'].update(visible=False)
                window_all_devices['-mark-as-resolved-'].update(visible=False)
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
            if show_main_table:
                selected_device = table_data[values['-all-devices-'][0]]
            else:
                selected_device = filter_table_data[values['-all-devices-'][0]]
            if selected_device:
                # print(selected_device)
                window_all_devices['-modify-device-button-'].update(visible=selected_device[3] == 'false')
                window_all_devices['-faulty-report-device-button-'].update(visible=selected_device[3] == 'false')
                window_all_devices['-delete-device-button-'].update(visible=selected_device[3] == 'false')
                window_all_devices['-fault-details-'].update(visible=not selected_device[3] == 'false')
                window_all_devices['-mark-as-resolved-'].update(visible=not selected_device[3] == 'false')
        if event == '-modify-device-button-':
            modify_device(selected_device, idToken)
            window_all_devices['-modify-device-button-'].update(visible=False)
            window_all_devices['-faulty-report-device-button-'].update(visible=False)
            window_all_devices['-delete-device-button-'].update(visible=False)
            window_all_devices['-fault-details-'].update(visible=False)
            window_all_devices['-mark-as-resolved-'].update(visible=False)
        if event == '-faulty-report-device-button-':
            report_device(selected_device, idToken)
            window_all_devices['-modify-device-button-'].update(visible=False)
            window_all_devices['-faulty-report-device-button-'].update(visible=False)
            window_all_devices['-delete-device-button-'].update(visible=False)
            window_all_devices['-fault-details-'].update(visible=False)
            window_all_devices['-mark-as-resolved-'].update(visible=False)
        if event == '-fault-details-':
            fault_details(selected_device[0], idToken)
            window_all_devices['-modify-device-button-'].update(visible=False)
            window_all_devices['-faulty-report-device-button-'].update(visible=False)
            window_all_devices['-delete-device-button-'].update(visible=False)
            window_all_devices['-fault-details-'].update(visible=False)
            window_all_devices['-mark-as-resolved-'].update(visible=False)
        if event == '-mark-as-resolved-':
            db.child('devices').child(selected_device[0]).update(data={'isFaulty': 'false'}, token=idToken)
            db.child('faulty_devices').child(selected_device[0]).remove(token=idToken)
            storage.delete(name=f"{selected_device[0]}.png", token=idToken)
            if path.exists(path.join(user_data_location, 'download.png')):
                os.remove(path.join(user_data_location, 'download.png'))
            window_all_devices['-modify-device-button-'].update(visible=False)
            window_all_devices['-faulty-report-device-button-'].update(visible=False)
            window_all_devices['-delete-device-button-'].update(visible=False)
            window_all_devices['-fault-details-'].update(visible=False)
            window_all_devices['-mark-as-resolved-'].update(visible=False)
        if event == '-filter-submit-button-' or event == '-filter-query-' + '_Enter':
            query = values['-filter-query-']
            if len(query):
                window_all_devices['-filter-query-'].update(value="")
                filter_table_data = search_devices(table_data, query)
                window_all_devices['-all-devices-'].update(values=filter_table_data)
                show_main_table = False
            else:
                window_all_devices['-all-devices-'].update(values=table_data)
                show_main_table = True
        if event == 'Logout':
            window_all_devices.close()
            if path.exists(path.join(user_data_location, 'auth.json')):
                os.remove(path.join(user_data_location, 'auth.json'))
            show_main_screen()
        if event == 'Student name tag':
            student_name_tag_window.student_name_tag()
        if event == 'Device QR Code tag':
            device_tag_window.device_tag()
        if event == 'Devices':
            csv_file_path = sg.popup_get_file(message='Upload device csv file(s)', title='Device file uploader',
                                              font=font_normal, keep_on_top=True, file_types=(('CSV Files', '*.csv'),),
                                              icon=image_to_base64(resource_path(path.join('assets', 'logo.png'))),
                                              multiple_files=True)
            if csv_file_path:
                thread_device_upload = Thread(target=add_device_to_database,
                                              args=(window_all_devices, csv_file_path, idToken))
                thread_device_upload.start()
        if event == 'Update account':
            pass
        if event == '-table-item-delete-' and values[event] == 'full-table' and show_main_table:
            window_all_devices['-all-devices-'].update(values=table_data)
            sg.popup_quick_message('Device deleted successfully.', auto_close_duration=1, font=font_normal)
        if event == '-table-item-delete-' and values[event] == 'filter-table' and not show_main_table:
            window_all_devices['-all-devices-'].update(values=filter_table_data)
            sg.popup_quick_message('Device deleted successfully.', auto_close_duration=1, font=font_normal)
        if event == '-table-delete-':
            window_all_devices['-all-devices-'].update(values=table_data)
        if event == '-table-item-update-' and values[event] == 'full-table' and show_main_table:
            window_all_devices['-all-devices-'].update(values=table_data)
            sg.popup_quick_message('Device updated successfully.', auto_close_duration=1, font=font_normal)
        if event == '-table-item-update-' and values[event] == 'filter-table' and not show_main_table:
            window_all_devices['-all-devices-'].update(values=filter_table_data)
            sg.popup_quick_message('Device updated successfully.', auto_close_duration=1, font=font_normal)
        if event == '-table-item-added-':
            window_all_devices['-all-devices-'].update(values=table_data)
        if event == 'Download device list CSV file template':
            with open(path.join(Path.home(), 'Downloads', 'device_list_csv_template.csv'), mode='w',
                      newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Device name', 'device type', 'device sub-type', 'location', 'purpose'])
            sg.popup_quick_message('Checkout the download folder for the template file', auto_close_duration=1,
                                   font=font_normal)
        if event == 'Download student booking CSV file template':
            with open(path.join(Path.home(), 'Downloads', 'student_booking_csv_template.csv'), mode='w',
                      newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Email', 'FirstName', 'LastName', 'Preferred name (if any)', 'Role (student/teacher)'])
            sg.popup_quick_message('Checkout the download folder for the template file', auto_close_duration=1,
                                   font=font_normal)
        if event == 'Borrowed device list':
            show_borrow_window = False
            if not path.exists(path.join(user_data_location, 'booking.json')):
                borrow_file_path = sg.popup_get_file(message='Choose student booking csv file(s)',
                                                     title='Borrower details', font=font_normal, keep_on_top=True,
                                                     file_types=(('CSV Files', '*.csv'),),
                                                     icon=image_to_base64(
                                                         resource_path(path.join('assets', 'logo.png'))),
                                                     multiple_files=True)
                if borrow_file_path:
                    create_json_file(borrow_file_path)
                    borrower_list_window.borrowed_devices_window(idToken)
            else:
                show_borrow_window = True

            if show_borrow_window:
                borrower_list_window.borrowed_devices_window(idToken)

    if thread_device_upload is not None:
        thread_device_upload.join()
    if thread_download_csv is not None:
        thread_download_csv.join()
    if thread_student_qrcode is not None:
        thread_student_qrcode.join()
    if path.exists(path.join(user_data_location, 'download.png')):
        os.remove(path.join(user_data_location, 'download.png'))
    if my_stream:
        my_stream.close()
    if path.exists(path.join(user_data_location, 'auth.json')):
        os.remove(path.join(user_data_location, 'auth.json'))
    window_all_devices.close()

