import PySimpleGUI as sg
from helper_lib.base64image import image_to_base64
from helper_lib.pathmaker import resource_path
from firebase.config import *
from PIL import Image
import io
import json
from datetime import datetime
from constant.global_info import *


def resize_image(filepath, max_size=300):
    image = Image.open(filepath)
    width, height = image.size
    if width > height:
        new_width = max_size
        new_height = int(max_size * height / width)
    else:
        new_height = max_size
        new_width = int(max_size * width / height)

    new_image = image.resize((new_width, new_height))
    with io.BytesIO() as bio:
        new_image.save(bio, format='PNG')
        return bio.getvalue()


def fault_details(selected_device_id, idToken):
    sg.theme('Material1')
    storage.child(f'/{selected_device_id}.png').download(path='/',
                                                         token=idToken,
                                                         filename=path.join(user_data_location, 'download.png'))
    description = db.child('faulty_devices').child(selected_device_id).get(token=idToken).val()
    # move('download.png', path.join('data', 'download.png'))
    layout = [[sg.Push(), sg.Image(data=resize_image(path.join(user_data_location, 'download.png'))), sg.Push()],
              [sg.Text('Fault details', font=font_normal)],
              [sg.Push(), sg.Multiline(key='-description-', expand_x=True, default_text=description['description'],
                                       size=(100, 10), autoscroll=True, disabled=True, font=font_normal), sg.Push()],
              [sg.Text('Add update', font=font_normal)],
              [sg.Input(key='-updates-', expand_x=True, font=font_normal)],
              [sg.Push(), sg.Button(button_text='Add update', key='-add-update-', font=font_normal), sg.Push()],
              ]

    window = sg.Window(title='CTS CMS :: Fault details', layout=layout, keep_on_top=True,
                       icon=image_to_base64(resource_path(path.join('assets', 'logo.png'))), finalize=True,
                       font=font_normal)

    msg = ''
    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == '-add-update-':
            if path.exists(path.join(user_data_location, 'auth.json')):
                user = json.load(open(path.join(user_data_location, 'auth.json'), ))
                if user:
                    email = user['email']
                    added_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    msg = f'Added by {email} at {added_at}\n'
            faulty_device_data = {
                "description": msg + values['-updates-'] + '\n\n' + description['description']
            }
            db.child('faulty_devices').child(selected_device_id).update(data=faulty_device_data, token=idToken)
            sg.popup_quick_message('Fault updates added successfully', auto_close_duration=1, font=font_normal)
            break
    window.close()
