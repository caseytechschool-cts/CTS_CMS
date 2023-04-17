import PySimpleGUI as sg
from firebase.config import *
from helper_lib.base64image import image_to_base64
from helper_lib.pathmaker import resource_path
from datetime import datetime
import json
from os import path
from threading import Thread
import win32com.client as win32
from constant.global_info import *


def thread_device_report(description, selected_device, idToken, fpath, window):
    msg = ''
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
        "description": msg + description if description else ''
    }
    db.child('devices').child(selected_device).update(data=device_data, token=idToken)
    db.child('faulty_devices').child(selected_device).set(data=faulty_device_data, token=idToken)
    storage.child(f'/{selected_device}.png').put(file=fpath, token=idToken)
    window.write_event_value('-thread-device-report-', 'done')


def thread_email(to, fpath, description, device_details):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.Subject = '[Action required] Faulty device report'
    mail.To = to
    attachment = mail.Attachments.Add(fpath)
    attachment.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", "device_img")
    device_id = device_details[0]
    device_name = device_details[5]
    device_type = device_details[1]
    device_sub_type = device_details[2]
    device_location = device_details[4]
    mail.HTMLBody = r"""
    Dear Admin,<br><br>
    The following information is added to the faulty device list.<br><br>
    Fault details: <br><br>
    {0}<br><br>
    <img src="cid:device_img" alt="faulty device image" width="400" height="auto"><br><br>
    Device details: <br><br>
    Device id: {1} <br>
    Device name: {2} <br>
    Device type: {3} <br>
    Device sub type: {4} <br>
    Device location: {5} <br><br>
    Regards,<br>
    CTS CMS Team
    """.format(description, device_id, device_name, device_type, device_sub_type, device_location)
    mail.Display()


def report_device(selected_device, idToken):
    sg.theme('Material1')
    layout = [[sg.Text('Brief description of the problem', font=font_normal)],
              [sg.Multiline(key='-description-', expand_x=True, size=(100, 5), autoscroll=True, font=font_normal)],
              [sg.Push(), sg.Text('Add images', font=font_normal), sg.Input(key='-path-', font=font_normal),
               sg.FileBrowse(), sg.Push()],
              [sg.Push(), sg.Button(button_color='#fcb116', button_text='Submit', font=font_normal),
               sg.Cancel(font=font_normal), sg.Push()],
              [sg.Text('Please upload a png or jpeg image file', key='-warning-', visible=False, font=font_normal)]
              ]

    window = sg.Window('Report as faulty', layout, element_justification='l', keep_on_top=True, font=font_normal,
                       icon=image_to_base64(resource_path(path.join('../assets', 'logo.png'))), finalize=True)

    thread_device = None
    thread_send_email = None
    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == 'Submit':
            if values['-path-'] == '':
                window['-warning-'].update(visible=True)
            else:
                _, ext = path.splitext(values['-path-'])
                if ext.lower() in ('.png', '.jpg', '.jpeg'):
                    window['-warning-'].update(visible=False)
                    thread_device = Thread(target=thread_device_report,
                                           args=(values['-description-'], selected_device[0], idToken, values['-path-'],
                                                 window)).start()
                else:
                    window['-warning-'].update(visible=True)
        if event == '-thread-device-report-' and values[event] == 'done':
            sg.popup_quick_message('Faulty device reported successfully!', auto_close_duration=1)
            button = sg.popup_ok_cancel('Do you want to send an email to report the fault?', keep_on_top=True,
                                        font=font_normal)
            if button == 'Cancel':
                break
            else:
                thread_send_email = Thread(target=thread_email, args=(EMAIL_TO, values['-path-'],
                                                                      values['-description-'], selected_device)).start()
                break

    if thread_device is not None:
        thread_device.join()
    if thread_send_email is not None:
        thread_send_email.join()
    window.close()
