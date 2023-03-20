import PySimpleGUI as sg


def borrow_and_return_page_layout():
    image_data = 'iVBORw0KGgoAAAANSUhEUgAAASwAAAEsCAYAAAB5fY51AAAC+UlEQVR42u3UQREAAAjDMFCO9KEDLpHQR7uSKYAD2rAAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAADAswLADDAjAswLAADAvAsADDAjAsAMMCDAvAsAAMCzAsAMMCMCzAsAAMCzAswwIMC8CwAMMCMCwAwwIMC8CwAAwLMCwAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAADAswLADDAjAswLAADAvAsADDAjAswLAMCzAsAMMCDAvAsAAMCzAsAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAAwLMCwAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAAwzIswLAADAswLADDAjAswLAADAvAsADDAjAsAMMCDAvAsAAMCzAsAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAAwLMCwAwwIMSwbAsAAMCzAsAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAAwLMCwAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAADAswLADDAgwLwLAADAswLADDAjAswLAADAvAsADDAjAsAMMCDAvAsAAMCzAsAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAAwLMCwAwwIMC8CwAAwLMCwAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAADAswLADDAjAswLAADAvAsADDAjAsAMMCDAvAsAAMCzAsAMMCDAvAsAAMCzAsAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAAwLMCwAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAADAswLADDAgwLwLAADAswLADDAjAswLAADAvAsADDAjAsAMMCDAvAsAAMCzAsAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAMMyLMCwAAwLMCwAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAADAswLADDAjAswLAADAvAsADDAjAsAMMCDAvAsAAMCzAsAMMCDMuwAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAAwL+GwB2Mfrx/xgE7oAAAAASUVORK5CYII='
    font = ('Century Gothic', 20, 'bold')
    student_main_screen_layout = [
        [sg.Push(), sg.Button(button_text='Borrow Item', key='-borrow_item-', font=font, size=20), sg.Push()],
        [sg.Push(), sg.Button(button_text='Return Item', key='-return_item-', font=font, size=20), sg.Push()]
    ]

    scan_student_qr_code = [[sg.Button(button_text='Scan student QRcode', size=20, font=font, key='-borrow_student_id-')]]
    scan_item_qr_code = [[sg.Button(button_text='Scan item QRcode', size=20, font=font, key='-borrow_device_id-')]]

    student_borrow_screen_layout = [
        [sg.Push(), sg.Image(size=(300, 300), key='-qrcode1-', data=image_data), sg.Push()],
        [sg.Column(scan_student_qr_code, key='-col_borrow_student_id-', visible=True),
         sg.Column(scan_item_qr_code, key='-col_borrow_device_id-', visible=False)]
    ]

    student_device_return_layout = [
        [sg.Push(), sg.Image(size=(300, 300), key='-qrcode2-', data=image_data), sg.Push()],
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



