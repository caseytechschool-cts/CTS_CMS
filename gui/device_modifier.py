import PySimpleGUI as sg
from firebase.config import *
from helper_lib.base64image import image_to_base64
from helper_lib.pathmaker import resource_path
from os import path
from constant.global_info import *


def modify_device(selected_device, idToken):
    sg.theme('Material1')
    layout = [[sg.Text('Device name', font=font_normal), sg.Input(key='-NAME-', default_text=selected_device[5],
                                                                  font=font_normal)],
              [sg.Text('Device type', font=font_normal), sg.Input(key='-TYPE-', default_text=selected_device[2],
                                                                  font=font_normal)],
              [sg.Text('Device sub-type', font=font_normal), sg.Input(key='-SUB-TYPE-', default_text=selected_device[1],
                                                                      font=font_normal)],
              [sg.Text('Device location', font=font_normal), sg.Input(key='-LOCATION-', default_text=selected_device[4],
                                                                      font=font_normal)],
              [sg.Button(button_color='#2db52c', button_text='Submit', font=font_normal), sg.Cancel(font=font_normal)]]

    window = sg.Window('Modify device', layout, element_justification='r', keep_on_top=True, font=font_normal,
                       icon=image_to_base64(resource_path(path.join('../assets', 'logo.png'))), finalize=True)

    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == 'Submit':
            device_data = {
                "name": values['-NAME-'],
                "device_type": values['-TYPE-'],
                "device_sub_type": values['-SUB-TYPE-'],
                "location": values['-LOCATION-']
            }
            db.child('devices').child(selected_device[0]).update(data=device_data, token=idToken)
            sg.popup_quick_message('Device updated successfully!', auto_close_duration=1)
            break
    window.close()
