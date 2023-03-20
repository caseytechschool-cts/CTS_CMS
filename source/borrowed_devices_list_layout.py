import PySimpleGUI as sg
from borrow_device import borrowed_devices_list


def borrowed_devices_tab_layout(): 
    font = ('Century Gothic', 20, 'bold')
    data_table = borrowed_devices_list()
    headings = ['Student ID', 'Device ID']
    layout_borrowed_devices = [
        [sg.Table(values=[[]], headings=headings, key='-borrowed_devices_tab-', justification='center',
                  row_height=30, alternating_row_color='#b5c1ca', expand_x=True, expand_y=True, visible=False)],
        [sg.Text(text='No device found', key='-no_borrowed_device-', visible=True, expand_x=True, expand_y=True,
                 justification='c', font=font)]
    ]
    return layout_borrowed_devices
