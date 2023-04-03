import PySimpleGUI as sg
from firebase.config import *
from helper_lib.base64image import image_to_base64


def modify_device(selected_device, idToken):
    sg.theme('Material1')
    layout = [[sg.Text('Device name'), sg.Input(key='-NAME-', default_text=selected_device[5])],
              [sg.Text('Device type'), sg.Input(key='-TYPE-', default_text=selected_device[2])],
              [sg.Text('Device sub-type'), sg.Input(key='-SUB-TYPE-', default_text=selected_device[1])],
              [sg.Text('Device location'), sg.Input(key='-LOCATION-', default_text=selected_device[4])],
              [sg.OK(button_color='#2db52c'), sg.Cancel()]]

    window = sg.Window('Modify device', layout, element_justification='r', keep_on_top=True,
                       icon=image_to_base64('logo.png'), finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == 'OK':
            device_data = {
                "name": values['-NAME-'],
                "device_type": values['-TYPE-'],
                "device_sub_type": values['-SUB-TYPE-'],
                "location": values['-LOCATION-']
            }
            db.child('devices').child(selected_device[0]).update(data=device_data, token=idToken)
            sg.popup_notify('Device updated successfully!')
            break
    window.close()
