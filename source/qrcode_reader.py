import cv2
import os


def read_qrcode():
    folder_path = '../QRCode'
    os.chdir(folder_path)

    for file in os.listdir():
        if file.endswith('.png'):
            file_path = os.path.join(folder_path, file)

            img = cv2.imread(file_path)
            detector = cv2.QRCodeDetector()
            data, bbox, straight_qrcode = detector.detectAndDecode(img)
            if bbox is not None:
                print(data)
        # return data