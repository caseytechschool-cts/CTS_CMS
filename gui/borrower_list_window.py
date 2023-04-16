import PySimpleGUI as sg
from helper_lib.base64image import image_to_base64
import json
import csv
from os import path, remove
from helper_lib.search import search_devices
import ast


font_underline = ('Century Gothic', 10, 'underline')
font_normal = ('Century Gothic', 10, '')
table_heading = ['Device ID', 'Borrower name', 'Borrower role', 'Device name']
table_data = []
filter_table_data = []
window_borrower_list = None
json_data = None


def get_device_list_from_stream(device_list):
    global table_data
    for key, val in device_list.items():
        borrow_data = ast.literal_eval(val.items())
        borrow_data.insert(0, key)
        t = student_id_to_data(borrow_data[1])
        borrow_data.insert(2, t[2].capitalize())
        if t[1] != "":
            borrow_data[1] = t[1]
        else:
            borrow_data[1] = t[0]
        table_data.append(borrow_data)

    window_borrower_list.write_event_value('-table-item-added-', 'full-table')


def add_device_to_table_data(device_id, row_data):
    borrow_data = ast.literal_eval(row_data.items())
    borrow_data.insert(0, device_id)
    t = student_id_to_data(borrow_data[1])
    borrow_data.insert(2, t[2].capitalize())
    if t[1] != "":
        borrow_data[1] = t[1]
    else:
        borrow_data[1] = t[0]
    table_data.append(borrow_data)
    window_borrower_list.write_event_value('-table-item-added-', 'full-table')


def delete_item_from_table(device_id):
    change_main_table = False
    change_filterred_table = False
    for index in range(len(table_data)):
        if table_data[index][0] == device_id:
            del table_data[index]
            change_main_table = True
            break
    if change_main_table:
        window_borrower_list.write_event_value('-table-item-delete-', 'full-table')

    for index in range(len(filter_table_data)):
        if filter_table_data[index][0] == device_id:
            del filter_table_data[index]
            change_filterred_table = True
            break
    if change_filterred_table:
        window_borrower_list.write_event_value('-table-item-delete-', 'filter-table')


def stream_handler(message):
    # print(message['event'], message['data'], message['path'])
    if message['event'] == 'put' and isinstance(message['data'], type(None)) and message['path'] != '/':
        document_id = message['path'][1:]
        delete_item_from_table(document_id)
    elif message['event'] == 'put' and isinstance(message['data'], type(None)) and message['path'] == '/':
        global table_data
        table_data = []
        window_borrower_list.write_event_value('-table-delete-', 'all')
    elif message['event'] == 'put' and isinstance(message['data'], dict) and message['path'] != '/':
        add_device_to_table_data(message['path'][1:], message['data'])
    elif message['event'] == 'put' and isinstance(message['data'], dict):
        get_device_list_from_stream(message['data'])


def student_id_to_data(student_id='1b5cce5b-65bb-4fc0-8533-3a44d6bb1bc5'):
    if json_data:
        try:
            return json_data[student_id]
        except KeyError:
            if path.exists(path.join('../csv_files', 'booking.json')):
                remove(path.join('../csv_files', 'booking.json'))
    return None


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

    with open(path.join('../csv_files', 'booking.json'), 'w') as fp:
        json.dump(students, fp)


def borrowed_devices_window(idToken=None):
    sg.theme('Material1')
    show_main_table = True
    header_padding = ((5, 5), (20, 20))
    global table_data, json_data, filter_table_data
    # my_stream = db.child("borrowed_devices").stream(stream_handler, token=idToken)
    if path.exists(path.join('../csv_files', 'booking.json')):
        with open(path.join('../csv_files', 'booking.json')) as f:
            json_data = json.load(f)
    student_id_to_data()
    layout = [
        [sg.Push(), sg.Text(text='Choose the current student booking csv file(s) for student details',
                            font=font_normal, key='-msg-', visible=True), sg.Push()],
        [sg.Push(), sg.Input(default_text='', key='-booking-files-', visible=True),
         sg.FilesBrowse(key='-files-', file_types=(('CSV Files', '*.csv'),), visible=True), sg.Push()],
        [sg.Push(), sg.ButtonMenu('  Choose option  ', menu_def=['Options', ['Student::-student-', 'Staff::-staff-']],
                                  key='-choose-option-', background_color='white', pad=header_padding),
         sg.Input(default_text='', key='-filter-people-', do_not_clear=True, pad=header_padding),
         sg.Button(button_text='  Filter  ', key='-filter-people-button-', pad=header_padding),
         sg.Push()],
        [sg.Table(values=table_data, headings=table_heading, key='-borrower-list-', justification='center',
                  alternating_row_color='#b5c1ca', expand_x=True, expand_y=True, row_height=20, enable_events=True,
                  auto_size_columns=True, vertical_scroll_only=False, display_row_numbers=True,
                  visible_column_map=[False, True, True, True])],
        [sg.Sizegrip()]
    ]

    max_width, max_height = sg.Window.get_screen_size()
    max_width = int(max_width * 0.8)
    max_height = int(max_height * 0.6)
    global window_borrower_list
    window_borrower_list = sg.Window(title="CTS CMS",
                                     layout=layout,
                                     size=(max_width, max_height),
                                     icon=image_to_base64('logo.png'),
                                     finalize=True,
                                     resizable=True)

    window_borrower_list['-filter-people-'].bind('<Return>', '_Enter')

    while True:
        event, values = window_borrower_list.read(timeout=300)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if path.exists(path.join('../csv_files', 'booking.json')):
            window_borrower_list['-msg-'].update(visible=False)
            window_borrower_list['-booking-files-'].update(visible=False)
            window_borrower_list['-files-'].update(visible=False)
        if values['-booking-files-']:
            student_csv_files = values['-booking-files-']
            window_borrower_list['-booking-files-'].update(value=None)
            create_json_file(student_csv_files)
        if event == '-filter-people-button-' or event == '-filter-people-' + '_Enter':
            query = values['-filter-people-']
            if len(query):
                window_borrower_list['-filter-people-'].update(value="")
                filter_table_data = search_devices(table_data, query)
                window_borrower_list['-borrower-list-'].update(values=filter_table_data)
                show_main_table = False
            else:
                window_borrower_list['-borrower-list-'].update(values=table_data)
                show_main_table = True
        if event == '-table-item-delete-' and values[event] == 'full-table' and show_main_table:
            window_borrower_list['-borrower-list-'].update(values=table_data)
            # sg.popup_quick_message('Device deleted successfully.', auto_close_duration=1)
        if event == '-table-item-delete-' and values[event] == 'filter-table' and not show_main_table:
            window_borrower_list['-borrower-list-'].update(values=filter_table_data)
            # sg.popup_quick_message('Device deleted successfully.', auto_close_duration=1)
        if event == '-table-delete-':
            window_borrower_list['-borrower-list-'].update(values=table_data)
        if event == '-table-item-added-':
            window_borrower_list['-borrower-list-'].update(values=table_data)

    # my_stream.close()
    window_borrower_list.close()


if __name__ == '__main__':
    borrowed_devices_window()
