import PySimpleGUI as sg


def borrow_and_return_page_layout():
    font = ('Century Gothic', 20, 'bold')
    student_main_screen_layout = [
        [sg.Push(), sg.Button(button_text='Borrow Item', key='-borrow_item-', font=font, size=20), sg.Push()],
        [sg.Push(), sg.Button(button_text='Return Item', key='-return_item-', font=font, size=20), sg.Push()]
    ]

    scan_student_qr_code = [[sg.Button(button_text='Scan student QRcode', size=20, font=font, key='-borrow_student_id-')]]
    scan_item_qr_code = [[sg.Button(button_text='Scan item QRcode', size=20, font=font, key='-borrow_device_id-')]]

    student_borrow_screen_layout = [
        [sg.Push(), sg.Image(size=(300, 300), key='-qrcode-'), sg.Push()],
        [sg.Column(scan_student_qr_code, key='-col_borrow_student_id-', visible=False),
         sg.Column(scan_item_qr_code, key='-col_borrow_device_id-', visible=True)]
    ]

    student_device_return_layout = [
        [sg.Push(), sg.Image(size=(300, 300), key='-qrcode-'), sg.Push()],
        [sg.Push(), sg.Button(button_text='Scan item QRcode to return', size=30, font=font, key='-device_return-'), sg.Push()]
    ]

    layout_student = [
        [sg.VPush()],
        [sg.Column(student_main_screen_layout, key='-student_main_screen-', visible=True),
         sg.Column(student_borrow_screen_layout, key='-student_borrow_screen-', visible=False),
         sg.Column(student_device_return_layout, key='-student_device_return_screen-', visible=False)],
        [sg.VPush()]
    ]

    return layout_student



