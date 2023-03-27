import PySimpleGUI as sg

from gui.main import show_login_screen
from student_tab_layout import borrow_and_return_page_layout
from borrowed_devices_list_layout import borrowed_devices_tab_layout
from helper_lib.base64image import image_to_base64
from menu import default_menu
from qr_code.qrcode_reader import read_student_qrcode_from_webcam, read_device_qrcode_from_webcam, return_device_qrcode_webcam
from firebase.borrow_device import borrowed_devices_list
from show_device_list import show_device_list_window


def main():
    sg.theme('Material1')
    menu_background_color = '#ffffff'

    layout = [
        [sg.Menu(default_menu(), key='-menu-', background_color=menu_background_color)],
        [sg.TabGroup([[sg.Tab('Borrow and return', borrow_and_return_page_layout(), element_justification='c')],
                      [sg.Tab('Borrowed devices', borrowed_devices_tab_layout(), element_justification='c')]],
                     tab_location='centertop', expand_x=True, expand_y=True)]
    ]
    window = sg.Window(title="Casey Tech School CMS",
                       layout=layout,
                       size=(800, 600),
                       icon=image_to_base64('logo.png'),
                       finalize=True)

    while True:
        event, values = window.read(timeout=100)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        print(event)
        if event == '-borrow_item-':
            window['-student_main_screen-'].update(visible=False)
            window['-student_device_return_screen-'].update(visible=False)
            window['-student_borrow_screen-'].update(visible=True)
        if event == '-return_item-':
            window['-student_main_screen-'].update(visible=False)
            window['-student_borrow_screen-'].update(visible=False)
            window['-student_device_return_screen-'].update(visible=True)
        if event == '-borrow_student_id-':
            student_qr_code = read_student_qrcode_from_webcam(window)
        if event == '-borrow_device_id-':
            read_device_qrcode_from_webcam(window, student_qr_code)
            borrowed_data_table = borrowed_devices_list()
            table_visible = any(borrowed_data_table)
            msg_visible = not table_visible
            window['-borrowed_devices_tab-'].update(values=borrowed_data_table, visible=table_visible)
            window['-no_borrowed_device-'].update(visible=msg_visible)
        if event == '-device_return-':
            return_device_qrcode_webcam(window)
            borrowed_data_table = borrowed_devices_list()
            table_visible = any(borrowed_data_table)
            msg_visible = not table_visible
            window['-borrowed_devices_tab-'].update(values=borrowed_data_table, visible=table_visible)
            window['-no_borrowed_device-'].update(visible=msg_visible)
            sg.popup_notify(title='Device return is successful')
        if event == 'Show device list':
            show_device_list_window()
        if event == 'Show faulty device list':
            show_login_screen()


if __name__ == '__main__':
    main()
