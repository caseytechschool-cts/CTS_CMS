import PySimpleGUI as sg
from helper_lib.base64image import image_to_base64
from os import path
from nametag.tag_generator import generate_name_tags
from threading import Thread


def student_name_tag():
    sg.theme('Material1')
    col1_layout = [
        [sg.Text('Upload student booking csv file(s)')],
        [sg.Input(key='-NAME-'),
         sg.FilesBrowse(file_types=(("CSV Files", "*.csv"),), key='-files-', size=(len('Browse') + 5, 1))],
        [sg.Text('Choose a folder to save name tags')],
        [sg.Input(key='-dest-folder-'),
         sg.FolderBrowse('Choose a folder', key='-dest-folder-', enable_events=True)],
        [sg.Text('Choose options:')],
        [sg.Checkbox(text='Add QR code', key='-add-qr-code-', default=True,
                     enable_events=True)],
        [sg.Checkbox(text='Add media permission box', key='-add-box-', default=True,
                     enable_events=True)],
        [sg.Push(), sg.Button(button_color='#2db52c', button_text='Submit', size=(len('Submit') + 5, 1)),
         sg.Cancel(size=(len('Cancel') + 5, 1)), sg.Push()],
        [sg.HSeparator(color='#808080', pad=((0, 0), (20, 10)))],
        [sg.Text(text='Generating ', key='-status-', text_color='#808080', visible=False)]
    ]
    col2_layout = [
        [sg.VPush()],
        [sg.Text('Sample name tag')],
        [sg.Image(key='-example-image-')],
        [sg.VPush()]
    ]
    layout = [
        [sg.Column(col1_layout, pad=((20, 20), (20, 20)), justification='l', element_justification='l'),
         sg.Column(col2_layout, pad=((20, 20), (20, 20)), justification='c', element_justification='c')]
    ]

    window = sg.Window('Name tag generator', layout, element_justification='l', keep_on_top=True,
                       icon=image_to_base64('logo.png'), finalize=True)

    thread_name_tag = None
    thread_name_tag_running = None
    while True:
        event, values = window.read(timeout=300)
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if values['-add-qr-code-'] and values['-add-box-']:
            window['-example-image-'].update(source=image_to_base64(path.join('../assets', 'qr_code_default.png')),
                                             size=(360, 130))
        elif values['-add-box-'] and not values['-add-qr-code-']:
            window['-example-image-'].update(source=image_to_base64(path.join('../assets', 'qr_code_name_box.png')),
                                             size=(360, 130))
        elif not values['-add-box-'] and values['-add-qr-code-']:
            window['-example-image-'].update(source=image_to_base64(path.join('../assets', 'qr_code_qr_name.png')),
                                             size=(360, 130))
        else:
            window['-example-image-'].update(source=image_to_base64(path.join('../assets', 'qr_code_name_only.png')),
                                             size=(360, 130))
        if event == 'Submit':
            window['-status-'].update(value='Generating ', visible=False)
            thread_name_tag_running = True
            Thread(target=generate_name_tags,
                   args=(values['-files-'], values['-dest-folder-'], values['-add-qr-code-'], values['-add-box-'],
                         window)).start()
        if thread_name_tag_running:
            window['-status-'].update(value=window['-status-'].get() + '.', visible=True)
        if event == '-thread-name-tags-' and values[event] == 'generated':
            window['-status-'].update(value='Generated successfully', visible=True)
            thread_name_tag_running = None

    if thread_name_tag is not None:
        thread_name_tag.join()
    window.close()


if __name__ == '__main__':
    student_name_tag()
