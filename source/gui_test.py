import os

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import PySimpleGUI as sg
from student_tab_layout import borrow_and_return_page_layout
from borrowed_devices_list_layout import borrowed_devices_tab_layout
from base64image import image_to_base64
from menu import default_menu, login_menu, super_user_menu_login
from borrow_device import borrow_item
import ast


def main():
    sg.theme('Material1')
    menu_background_color = '#ffffff'
    recording1 = False
    stop_recording1 = False
    recording2 = False
    stop_recording2 = False

    student_id = None
    device_data = None

    image_data = 'iVBORw0KGgoAAAANSUhEUgAAASwAAAEsCAYAAAB5fY51AAAC+UlEQVR42u3UQREAAAjDMFCO9KEDLpHQR7uSKYAD2rAAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAADAswLADDAjAswLAADAvAsADDAjAsAMMCDAvAsAAMCzAsAMMCMCzAsAAMCzAswwIMC8CwAMMCMCwAwwIMC8CwAAwLMCwAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAADAswLADDAjAswLAADAvAsADDAjAswLAMCzAsAMMCDAvAsAAMCzAsAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAAwLMCwAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAAwzIswLAADAswLADDAjAswLAADAvAsADDAjAsAMMCDAvAsAAMCzAsAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAAwLMCwAwwIMSwbAsAAMCzAsAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAAwLMCwAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAADAswLADDAgwLwLAADAswLADDAjAswLAADAvAsADDAjAsAMMCDAvAsAAMCzAsAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAAwLMCwAwwIMC8CwAAwLMCwAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAADAswLADDAjAswLAADAvAsADDAjAsAMMCDAvAsAAMCzAsAMMCDAvAsAAMCzAsAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAAwLMCwAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAADAswLADDAgwLwLAADAswLADDAjAswLAADAvAsADDAjAsAMMCDAvAsAAMCzAsAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAMMyLMCwAAwLMCwAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAADAswLADDAjAswLAADAvAsADDAjAsAMMCDAvAsAAMCzAsAMMCDMuwAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAAwL+GwB2Mfrx/xgE7oAAAAASUVORK5CYII='

    layout = [
        [sg.Menu(default_menu(), key='-menu-', background_color=menu_background_color)],
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

        if event == '-borrow_item-':
            # update window layout
            window['-student_main_screen-'].update(visible=False)
            window['-student_device_return_screen-'].update(visible=False)
            window['-student_borrow_screen-'].update(visible=True)
        if event == '-return_item-':
            window['-student_main_screen-'].update(visible=False)
            window['-student_borrow_screen-'].update(visible=False)
            window['-student_device_return_screen-'].update(visible=True)
        if event == '-borrow_student_id-':
            recording2 = False
            stop_recording2 = False
            recording1 = True
            camera_id = 1
            capture = cv2.VideoCapture(camera_id)  # , cv2.CAP_DSHOW
            detector = cv2.QRCodeDetector()
            capture.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
            capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

            while recording1:
                ret, frame = capture.read()
                qr_data, bbox, straight_qrcode = detector.detectAndDecode(frame)
                window['-qrcode1-'].update(data=cv2.imencode('.png', frame)[1].tobytes())
                window.refresh()

                if qr_data:
                    qr_data = ast.literal_eval(qr_data)
                    student_id = qr_data['id']
                    recording1 = False
                    stop_recording1 = True

        if stop_recording1:
            capture.release()
            stop_recording1 = False
            recording1 = False
            window['-qrcode1-'].update(data=image_data)
            window['-col_borrow_student_id-'].update(visible=False)
            window['-col_borrow_device_id-'].update(visible=True)

        if event == '-borrow_device_id-':
            print('I am here')
            recording1 = False
            stop_recording1 = False
            recording2 = True
            camera_id = 1
            capture = cv2.VideoCapture(camera_id)  # , cv2.CAP_DSHOW
            detector = cv2.QRCodeDetector()
            capture.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
            capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

            while recording2:
                ret, frame = capture.read()
                qr_data, bbox, straight_qrcode = detector.detectAndDecode(frame)
                window['-qrcode1-'].update(data=cv2.imencode('.png', frame)[1].tobytes())
                window.refresh()

                if qr_data:
                    print(qr_data)
                    device_data = ast.literal_eval(qr_data)
                    recording2 = False
                    stop_recording2 = True

        if stop_recording2:
            capture.release()
            stop_recording2 = False
            recording2 = False
            borrow_item(device_data=device_data, student_id=student_id)
            window['-qrcode1-'].update(data=image_data)
            window['-student_main_screen-'].update(visible=True)
            window['-student_device_return_screen-'].update(visible=False)
            window['-student_borrow_screen-'].update(visible=False)




if __name__ == '__main__':
    main()
