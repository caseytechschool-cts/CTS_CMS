import PySimpleGUI as sg
from helper_lib.base64image import image_to_base64
from helper_lib.pathmaker import resource_path
from nametag.tag_generator import generate_name_tags
from threading import Thread
from constant.global_info import *


def student_name_tag():
    sg.theme('Material1')
    destination_folder = path.join(Path.home(), 'Downloads')
    col1_layout = [
        [sg.Text('Upload student booking csv file(s)', font=font_normal)],
        [sg.Input(key='-NAME-', font=font_normal),
         sg.FilesBrowse(file_types=(("CSV Files", "*.csv"),), key='-files-', size=(len('Browse') + 5, 1),
                        font=font_normal)],
        [sg.Text('Choose a folder to save name tags', font=font_normal)],
        [sg.Input(key='-dest-folder-input-', font=font_normal, default_text=destination_folder),
         sg.FolderBrowse('Browse', key='-dest-folder-', enable_events=True, font=font_normal,
                         size=(len('Browse') + 5, 1))],
        [sg.Text('Choose options:', font=font_normal)],
        [sg.Checkbox(text='Add QR code', key='-add-qr-code-', default=True, font=font_normal,
                     enable_events=True)],
        [sg.Checkbox(text='Add media permission box', key='-add-box-', default=True, font=font_normal,
                     enable_events=True)],
        [sg.Push(), sg.Button(button_color='#2db52c', button_text='Submit', size=(len('Submit') + 5, 1), font=font_normal),
         sg.Cancel(size=(len('Cancel') + 5, 1), font=font_normal), sg.Push()],
        [sg.HSeparator(color='#808080', pad=((0, 0), (20, 10)))],
        [sg.Text(text='Generating ', key='-status-', text_color='#808080', visible=False, font=font_normal)]
    ]
    col2_layout = [
        [sg.VPush()],
        [sg.Text('Sample name tag', font=font_normal)],
        [sg.Image(key='-example-image-')],
        [sg.VPush()]
    ]
    layout = [
        [sg.Column(col1_layout, pad=((20, 20), (20, 20)), justification='l', element_justification='l'),
         sg.Column(col2_layout, pad=((20, 20), (20, 20)), justification='c', element_justification='c')]
    ]

    window = sg.Window(title='CTS CMS :: Name tag generator', layout=layout, element_justification='l',
                       keep_on_top=True, font=font_normal,
                       icon=image_to_base64(resource_path(path.join('assets', 'logo.png'))), finalize=True)

    thread_name_tag = None
    thread_name_tag_running = None
    while True:
        event, values = window.read(timeout=300)
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if values['-add-qr-code-'] and values['-add-box-']:
            window['-example-image-'].update(source=image_to_base64(resource_path(path.join('assets', 'qr_code_default.png'))),
                                             size=(360, 130))
        elif values['-add-box-'] and not values['-add-qr-code-']:
            window['-example-image-'].update(source=image_to_base64(resource_path(path.join('assets', 'qr_code_name_box.png'))),
                                             size=(360, 130))
        elif not values['-add-box-'] and values['-add-qr-code-']:
            window['-example-image-'].update(source=image_to_base64(resource_path(path.join('assets', 'qr_code_qr_name.png'))),
                                             size=(360, 130))
        else:
            window['-example-image-'].update(source=image_to_base64(resource_path(path.join('assets', 'qr_code_name_only.png'))),
                                             size=(360, 130))
        if event == 'Submit':
            window['-status-'].update(value='Generating ', visible=False)
            thread_name_tag_running = True
            thread_name_tag = Thread(target=generate_name_tags,
                                     args=(values['-files-'], values['-dest-folder-input-'], values['-add-qr-code-'],
                                           values['-add-box-'],
                                           window)).start()
        if thread_name_tag_running:
            window['-status-'].update(value=window['-status-'].get() + '.', visible=True)
        if event == '-thread-name-tags-' and values[event] == 'generated':
            window['-status-'].update(value='Generated successfully', visible=True)
            thread_name_tag_running = None
            break

    if thread_name_tag is not None:
        thread_name_tag.join()
    window.close()

