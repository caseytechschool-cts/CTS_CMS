import PySimpleGUI as sg
from firebase.config import *
from helper_lib.base64image import image_to_base64
from datetime import datetime
import json
from os import path


def report_device(selected_device, idToken):
    sg.theme('Material1')
    layout = [[sg.Text('Brief description of the problem')],
              [sg.Multiline(key='-description-', expand_x=True, size=(100, 5), autoscroll=True)],
              [sg.Push(), sg.Text('Add images'), sg.Input(key='-path-'), sg.FileBrowse(), sg.Push()],
              [sg.Push(), sg.Button(button_color='#fcb116', button_text='Submit'), sg.Cancel(), sg.Push()],
               [sg.Text('Please upload a png or jpeg image file', key='-warning-', visible=False)]
              ]

    window = sg.Window('Report as faulty', layout, element_justification='l', keep_on_top=True,
                       icon=image_to_base64('logo.png'), finalize=True)

    msg = ''
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == 'Submit':
            if values['-path-'] == '':
                window['-warning-'].update(visible=True)
            else:
                _, ext = path.splitext(values['-path-'])
                if ext.lower() in ('.png', '.jpg', '.jpeg'):
                    window['-warning-'].update(visible=False)
                    device_data = {
                        "isFaulty": True
                    }
                    if path.exists(path.join('../firebase', 'auth.json')):
                        user = json.load(open(path.join('../firebase', 'auth.json'), ))
                        if user:
                            email = user['email']
                            added_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            msg = f'Added by {email} at {added_at}\n'
                    faulty_device_data = {
                        "description": msg + values['-description-'] if values['-description-'] else ''
                    }
                    db.child('devices').child(selected_device[0]).update(data=device_data, token=idToken)
                    db.child('faulty_devices').child(selected_device[0]).set(data=faulty_device_data, token=idToken)
                    storage.child(f'/{selected_device[0]}.png').put(file=values['-path-'], token=idToken)
                    sg.popup_quick_message('Device reported successfully!', auto_close_duration=1)
                    break
                else:
                    window['-warning-'].update(visible=True)
    window.close()

