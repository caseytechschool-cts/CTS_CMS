import ast
import os

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
from firebase.borrow_device import borrow_item
from firebase.return_device import return_item

image_data = 'iVBORw0KGgoAAAANSUhEUgAAASwAAAEsCAYAAAB5fY51AAAC+UlEQVR42u3UQREAAAjDMFCO9KEDLpHQR7uSKYAD2rAAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAADAswLADDAjAswLAADAvAsADDAjAsAMMCDAvAsAAMCzAsAMMCMCzAsAAMCzAswwIMC8CwAMMCMCwAwwIMC8CwAAwLMCwAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAADAswLADDAjAswLAADAvAsADDAjAswLAMCzAsAMMCDAvAsAAMCzAsAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAAwLMCwAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAAwzIswLAADAswLADDAjAswLAADAvAsADDAjAsAMMCDAvAsAAMCzAsAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAAwLMCwAwwIMSwbAsAAMCzAsAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAAwLMCwAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAADAswLADDAgwLwLAADAswLADDAjAswLAADAvAsADDAjAsAMMCDAvAsAAMCzAsAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAAwLMCwAwwIMC8CwAAwLMCwAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAADAswLADDAjAswLAADAvAsADDAjAsAMMCDAvAsAAMCzAsAMMCDAvAsAAMCzAsAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAAwLMCwAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAADAswLADDAgwLwLAADAswLADDAjAswLAADAvAsADDAjAsAMMCDAvAsAAMCzAsAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAMMyLMCwAAwLMCwAwwIwLMCwAAwLwLAAwwIwLADDAgwLwLAADAswLADDAjAswLAADAvAsADDAjAsAMMCDAvAsAAMCzAsAMMCDMuwAMMCMCzAsAAMC8CwAMMCMCwAwwIMC8CwAAwL+GwB2Mfrx/xgE7oAAAAASUVORK5CYII='


def read_qrcode_from_path(sub_path: str) -> dict:
    folder_path = os.path.join('../QRCode', sub_path)
    os.chdir(folder_path)

    for file in os.listdir():
        if file.endswith('.png'):
            # file_path = os.path.join(folder_path, file)

            img = cv2.imread(file)
            detector = cv2.QRCodeDetector()
            data, bbox, straight_qrcode = detector.detectAndDecode(img)
            if bbox is not None:
                print(data)
        # return data


def read_student_qrcode_from_webcam(window) -> dict:
    recording = True
    stop_recording = False
    camera_id = 1
    capture = cv2.VideoCapture(camera_id)  # , cv2.CAP_DSHOW
    detector = cv2.QRCodeDetector()
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
    print(capture.isOpened())
    if capture.isOpened():
        while recording:
            ret, frame = capture.read()
            qr_data, bbox, straight_qrcode = detector.detectAndDecode(frame)
            window['-qrcode1-'].update(data=cv2.imencode('.png', frame)[1].tobytes())
            window.refresh()

            if qr_data:
                qr_data = ast.literal_eval(qr_data)
                recording = False
                stop_recording = True
    else:
        recording = False
        window['-student-id-scan-msg-'].update(value='Camera is not available.')

    if stop_recording:
        capture.release()
        stop_recording = False
        recording = False
        window['-qrcode1-'].update(data=image_data)
        window['-col_borrow_student_id-'].update(visible=False)
        window['-col_borrow_device_id-'].update(visible=True)
        window['-student-id-scan-msg-'].update(value=f"Hello {qr_data['first_name']} {qr_data['last_name']}")
        if qr_data:
            return qr_data
    return None


def read_device_qrcode_from_webcam(window, student_qr_code):
    recording = True
    stop_recording = False
    camera_id = 1
    capture = cv2.VideoCapture(camera_id)  # , cv2.CAP_DSHOW
    detector = cv2.QRCodeDetector()
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

    while recording:
        ret, frame = capture.read()
        qr_data, bbox, straight_qrcode = detector.detectAndDecode(frame)
        window['-qrcode1-'].update(data=cv2.imencode('.png', frame)[1].tobytes())
        window.refresh()

        if qr_data:
            print(qr_data)
            device_data = ast.literal_eval(qr_data)
            recording = False
            stop_recording = True

    if stop_recording:
        capture.release()
        stop_recording = False
        recording = False
        borrow_item(device_data=device_data, student_id=student_qr_code['id'])
        window['-qrcode1-'].update(data=image_data)
        window['-student_main_screen-'].update(visible=True)
        window['-student_device_return_screen-'].update(visible=False)
        window['-student_borrow_screen-'].update(visible=False)


def return_device_qrcode_webcam(window):
    recording = True
    stop_recording = False
    camera_id = 1
    capture = cv2.VideoCapture(camera_id)  # , cv2.CAP_DSHOW
    detector = cv2.QRCodeDetector()
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

    while recording:
        ret, frame = capture.read()
        qr_data, bbox, straight_qrcode = detector.detectAndDecode(frame)
        window['-qrcode2-'].update(data=cv2.imencode('.png', frame)[1].tobytes())
        window.refresh()

        if qr_data:
            print(qr_data)
            device_data = ast.literal_eval(qr_data)
            recording = False
            stop_recording = True

    if stop_recording:
        capture.release()
        stop_recording = False
        recording = False
        if device_data:
            return_item(device_data)
        window['-qrcode2-'].update(data=image_data)
        window['-student_main_screen-'].update(visible=True)
        window['-student_device_return_screen-'].update(visible=False)
        window['-student_borrow_screen-'].update(visible=False)
