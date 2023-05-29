import PySimpleGUI as sg
from helper_lib.base64image import image_to_base64
from helper_lib.pathmaker import resource_path
from nametag.tag_generator import generate_device_tags
from threading import Thread
from constant.global_info import *
from pathlib import Path


def device_tag(csv_files=''):
    sg.theme('Material1')
    destination_folder = path.join(Path.home(), 'Downloads')
    col1_layout = [
        [sg.Text('Upload device csv file(s)', font=font_normal)],
        [sg.Input(key='-NAME-', default_text=csv_files, font=font_normal),
         sg.FilesBrowse(file_types=(("CSV Files", "*.csv"),), key='-files-', size=(len('Browse') + 5, 1))],
        [sg.Text('Choose a folder to save name tags', font=font_normal)],
        [sg.Input(key='-dest-folder-input-', font=font_normal, default_text=destination_folder),
         sg.FolderBrowse('Browse', key='-dest-folder-', enable_events=True, font=font_normal,
                         size=(len('Browse') + 5, 1))],
        [sg.Text('Choose options:', font=font_normal)],
        [sg.Checkbox(text='Add device name', key='-add-device-name-', default=True, font=font_normal,
                     enable_events=True)],
        [sg.Push(), sg.Button(button_color='#2db52c', button_text='Submit', size=(len('Submit') + 5, 1),
                              font=font_normal),
         sg.Cancel(size=(len('Cancel') + 5, 1), font=font_normal), sg.Push()],
        [sg.HSeparator(color='#808080', pad=((0, 0), (20, 10)))],
        [sg.Text(text='Generating ', key='-status-', text_color='#808080', visible=False, font=font_normal)]
    ]
    col2_layout = [
        [sg.VPush()],
        [sg.Text('Sample device QR Code tag', font=font_normal)],
        [sg.Image(key='-example-image-')],
        [sg.VPush()]
    ]
    layout = [
        [sg.Column(col1_layout, pad=((20, 20), (20, 20)), justification='l', element_justification='l'),
         sg.Column(col2_layout, pad=((20, 20), (20, 20)), justification='c', element_justification='c')]
    ]

    window = sg.Window(title='CTS CMS :: Device QR Code generator', layout=layout, element_justification='l',
                       keep_on_top=True, icon=image_to_base64(resource_path(path.join('assets', 'logo.png'))),
                       finalize=True, font=font_normal)

    thread_device_tag = None
    thread_device_tag_running = None
    while True:
        event, values = window.read(timeout=300)
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if values['-add-device-name-']:
            window['-example-image-'].update(source=image_to_base64(resource_path(path.join('assets', 'device_tag_name.png'))),
                                             size=(240, 128))
        else:
            window['-example-image-'].update(source=image_to_base64(resource_path(path.join('assets', 'device_tag.png'))),
                                             size=(240, 128))
        if event == 'Submit':
            window['-status-'].update(value='Generating ', visible=False)
            thread_device_tag_running = True
            thread_device_tag = Thread(target=generate_device_tags,
                                       args=(values['-NAME-'], values['-dest-folder-input-'], values['-add-device-name-'],
                                             window)).start()
        if thread_device_tag_running:
            window['-status-'].update(value=window['-status-'].get() + '.', visible=True)
        if event == '-thread-device-tags-' and values[event] == 'generated':
            window['-status-'].update(value='Generated successfully', visible=True)
            thread_device_tag_running = None
            break

    if thread_device_tag is not None:
        thread_device_tag.join()
    window.close()

