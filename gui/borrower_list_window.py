import PySimpleGUI as sg
from helper_lib.base64image import image_to_base64

font_underline = ('Century Gothic', 10, 'underline')
font_normal = ('Century Gothic', 10, '')
table_heading = ['Device ID', 'Borrower name']
table_data = []
window_borrower_list = None


def borrowed_devices_window():
    sg.theme('Material1')
    header_padding = ((5, 5), (20, 20))
    global table_data
    layout = [
        [sg.Push(), sg.Text(text='Choose student booking csv file(s) for student details', font=font_normal), sg.Push()],
        [sg.Push(), sg.Input(default_text='', key='-booking-files-'),
         sg.FilesBrowse(key='-files-', file_types=(('CSV Files', '*.csv'),)), sg.Push()],
        [sg.Push(), sg.ButtonMenu('  Choose option  ', menu_def=['Options', ['Student::-student-', 'Staff::-staff-']],
                                  key='-choose-option-', background_color='white', pad=header_padding),
         sg.Input(default_text='', key='-filter-people-', do_not_clear=True, pad=header_padding),
         sg.Button(button_text='  Filter  ', key='-filter-people-button-', pad=header_padding),
         sg.Push()],
        [sg.Table(values=table_data, headings=table_heading, key='-borrower-list-', justification='center',
                  alternating_row_color='#b5c1ca', expand_x=True, expand_y=True, row_height=20, enable_events=True,
                  auto_size_columns=True, vertical_scroll_only=False, display_row_numbers=True)],
        [sg.Sizegrip()]
    ]

    max_width, max_height = sg.Window.get_screen_size()
    max_width = int(max_width * 0.8)
    max_height = int(max_height * 0.6)
    global window_borrower_list
    window_borrower_list = sg.Window(title="CTS CMS",
                                     layout=layout,
                                     size=(max_width, max_height),
                                     icon=image_to_base64('logo.png'),
                                     finalize=True,
                                     resizable=True)

    window_borrower_list['-filter-people-'].bind('<Return>', '_Enter')

    while True:
        event, values = window_borrower_list.read(timeout=100)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    window_borrower_list.close()


if __name__ == '__main__':
    borrowed_devices_window()
