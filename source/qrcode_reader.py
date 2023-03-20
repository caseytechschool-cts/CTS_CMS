import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import numpy as np


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


def read_qrcode_from_webcam() -> dict:
    camera_id = 1
    capture = cv2.VideoCapture(camera_id)
    detector = cv2.QRCodeDetector()
    done_detection = False
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
    while not done_detection:
        ret, frame = capture.read()
        cv2.imshow('QRcode',  frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        qr_data, bbox, straight_qrcode = detector.detectAndDecode(frame)
        print(qr_data)
        # print(bbox)
        if qr_data:
            # num_lines = len(bbox)
            # for i in range(num_lines):
            #     point1 = tuple(bbox[i][0])
            #     point2 = tuple(bbox[(i + 1) % num_lines][0])
            #     cv2.line(frame, point1, point2, color=(0, 255, 0), thickness=2)

            cv2.imshow('QRcode', frame)
            done_detection = not done_detection

    capture.release()
    cv2.destroyAllWindows()

    return qr_data


if __name__ == '__main__':
    print(read_qrcode_from_webcam())
