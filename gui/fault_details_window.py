import PySimpleGUI as sg
from helper_lib.base64image import image_to_base64
from firebase.config import *
from PIL import Image
import io


def resize_image(filepath, max_size=400):
    image = Image.open(filepath)
    width, height = image.size
    if width > height:
        new_width = max_size
        new_height = int(max_size * height/width)
    else:
        new_height = max_size
        new_width = int(max_size * width / height)

    new_image = image.resize((new_width, new_height))
    with io.BytesIO() as bio:
        new_image.save(bio, format='PNG')
        return bio.getvalue()


def fault_details(selected_device_id, idToken):
    sg.theme('Material1')

    storage.child('images').child(selected_device_id).download(path='/', filename='download.png', token=idToken)

    description = db.child('faulty_devices').child(selected_device_id).get(token=idToken).val()
    # image = resize_image('download.png')
    layout = [[sg.Push(), sg.Image(data=resize_image('download.png', max_size=600)), sg.Push()],
              [sg.Text('Fault details')],
              [sg.Push(), sg.Multiline(key='-description-', expand_x=True, default_text=description['description'],
                                       size=(100, 10)), sg.Push()],
              [sg.Push(), sg.Button(button_text='Add update', key='-add-update-'), sg.Push()],
              ]

    window = sg.Window('Fault details', layout, keep_on_top=True,
                       icon=image_to_base64('logo.png'), finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == '-add-update-':
            faulty_device_data = {
                "description": values['-description-'] if values['-description-'] else ''
            }
            db.child('faulty_devices').child(selected_device_id).update(data=faulty_device_data, token=idToken)
            sg.popup_notify('Updates are added successfully')
            break
    window.close()
