import PySimpleGUI as sg
from borrow_device import borrowed_devices_list


def borrowed_devices_tab_layout():
    font = ('Century Gothic', 20, 'bold')
    data_table = borrowed_devices_list()
    headings = ['Student ID', 'Device ID']
    layout_borrowed_devices = [
        [sg.Table(values=data_table, headings=headings, key='-borrowed_devices_tab-', justification='center',
                  expand_y=True, expand_x=True, row_height=30, alternating_row_color='#b5c1ca')]
    ]
    return layout_borrowed_devices