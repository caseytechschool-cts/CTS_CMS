from os import path, makedirs
import qrcode
from PIL import Image
import requests
import schedule
import time
import csv
import uuid
from config import *


def resize_QRcode(file_path, file_name, sub_path):
    dir_path = path.join('../../QRCode', sub_path, 'reSized')
    makedirs(dir_path, exist_ok=True)
    image = Image.open(file_path)
    image.thumbnail((100, 100))
    file_name = f"{file_name}_resized.png"
    file_path = path.join(dir_path, file_name)
    image.save(file_path)


def create_qrcode(data, id, sub_path):
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    file_name = f"{id}.png"
    file_path = path.join('../../QRCode', sub_path, file_name)
    img.save(file_path)
    resize_QRcode(file_path, id, sub_path)


def add_device_to_database(filename):
    with open(path.join('../../CSV', filename)) as devices:
        makedirs(path.join('../../QRCode', 'device'), exist_ok=True)
        csv_data = csv.reader(devices)
        line_count = 0
        for row in csv_data:
            if line_count:
                data = {
                    "name": row[0],
                    "device_type": row[1],
                    "device_sub_type": row[2],
                    "borrowed_by": "X"
                }
                device_id = db.child('devices').push(data)
                create_qrcode(data, device_id['name'], 'device')

            else:
                line_count = 1


def remove_device_from_database(user):
    pass


def read_device_list(user):
    pass


def read_device(user):
    pass


def update_device(user):
    pass


def user_log_in(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print(user)
    except requests.exceptions.HTTPError as error:
        print('Invalid email or password')
    except requests.exceptions.ConnectionError as error:
        print('Network problem')
    except requests.exceptions.Timeout as error:
        print('Request times out')






    # user = auth.refresh(user['refreshToken'])
    # print(user)
