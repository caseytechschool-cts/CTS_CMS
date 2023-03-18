from theme import theme_one
import PySimpleGUI as sg
from student_tab_layout import borrow_and_return_page_layout
from borrowed_devices_list_layout import borrowed_devices_tab_layout
from base64image import image_to_base64

# Add your dictionary to the PySimpleGUI themes
# sg.theme_add_new('Casey', theme_one)

# Switch your theme to use the newly added one
# sg.theme('LightPurple')


def main():
    # sg.theme("DefaultNoMoreNagging")
    sg.theme('Material1')

    layout = [
        [sg.TabGroup([[sg.Tab('Borrow and return', borrow_and_return_page_layout(), element_justification='c')],
                      [sg.Tab('Borrowed devices', borrowed_devices_tab_layout(), element_justification='c')]],
                     tab_location='centertop', expand_x=True, expand_y=True)]
    ]
    window = sg.Window(title="Casey Tech School CMS",
                       layout=layout,
                       size=(800, 600),
                       icon=image_to_base64('logo.png'),
                       finalize=True)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break


if __name__ == '__main__':
    main()

