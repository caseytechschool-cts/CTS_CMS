import PySimpleGUI as sg
from borrow_device import borrowed_devices_list


def borrowed_devices_tab_layout(): 
    font = ('Century Gothic', 20, 'bold')
    data_table = borrowed_devices_list()
    headings = ['Device ID', 'Student ID']
    table_visible = any(data_table)
    msg_visible = not table_visible

    layout_borrowed_devices = [
        [sg.Table(values=data_table, headings=headings, key='-borrowed_devices_tab-', justification='center',
                  row_height=30, alternating_row_color='#b5c1ca', expand_x=True, expand_y=True, visible=table_visible)],
        [sg.Text(text='No device found', key='-no_borrowed_device-', visible=msg_visible, expand_x=True, expand_y=True,
                 justification='c', font=font)]
    ]
    return layout_borrowed_devices
