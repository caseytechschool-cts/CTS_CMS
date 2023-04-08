import os

import qrcode
from os import path
from PIL import Image


def resize_QRcode(file_path, file_name, qr_save_path):
    image = Image.open(file_path)
    image.thumbnail((100, 100))
    file_name = f"{file_name}_resized.png"
    resized_file_path = path.join(qr_save_path, file_name)
    image.save(resized_file_path)
    if path.exists(file_path):
        os.remove(file_path)


def create_qrcode(csv_data, resource_id, qr_save_path):
    qr = qrcode.QRCode()
    qr.add_data(csv_data)
    qr.make(fit=True)
    img = qr.make_image()
    file_name = f"{resource_id}.png"
    file_path = path.join(qr_save_path, file_name)
    img.save(file_path)
    resize_QRcode(file_path, resource_id, qr_save_path)

