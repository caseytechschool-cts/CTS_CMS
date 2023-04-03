import PySimpleGUI as sg
from firebase.config import *
from helper_lib.base64image import image_to_base64
from PIL import Image
from os import path


def report_device(selected_device, idToken):
    sg.theme('Material1')
    layout = [[sg.Text('Brief description of the problem')],
              [sg.Multiline(key='-description-', expand_x=True, size=(100, 10))],
              [sg.Push(), sg.Text('Add images'), sg.Input(key='-path-'), sg.FileBrowse(), sg.Push()],
              [sg.Push(), sg.Button(button_color='#fcb116', button_text='Submit'), sg.Cancel(), sg.Push()]
              ]

    window = sg.Window('Report as faulty', layout, element_justification='l', keep_on_top=True,
                       icon=image_to_base64('logo.png'), finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == 'Submit':
            device_data = {
                "isFaulty": True
            }
            faulty_device_data = {
                "description": values['-description-'] if values['-description-'] else ''
            }
            db.child('devices').child(selected_device[0]).update(data=device_data, token=idToken)
            db.child('faulty_devices').child(selected_device[0]).set(data=faulty_device_data, token=idToken)
            if values['-path-']:
                extention = path.splitext(values['-path-'])[1].lower()
                print(extention)
                storage.child('images').child(selected_device[0]).put(file=values['-path-'], token=idToken)
            sg.popup_notify('Device reported successfully!')
            break
    window.close()
