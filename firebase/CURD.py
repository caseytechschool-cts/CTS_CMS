from os import path, makedirs
import requests
import csv
import json
from firebase.config import *
from qr_code.qrcode_generator import create_qrcode
from pathlib import Path


def add_device_to_database(filename: str, default=True) -> None:
    if default:
        dir_path = path.join('../CSV', filename)
        qr_save_path = path.join('../QRCode', 'device')
        makedirs(qr_save_path, exist_ok=True)
    else:
        dir_path = filename
        qr_save_path = path.join(Path.home(), 'Downloads', 'Devices QRcode')
        makedirs(qr_save_path, exist_ok=True)

    with open(dir_path) as devices:
        csv_data = csv.reader(devices)
        line_count = 0
        for row in csv_data:
            if line_count:
                device_data = {
                    "name": row[0],
                    "device_type": row[1],
                    "device_sub_type": row[2],
                    "isFaulty": False,
                    "location": row[3]
                }
                device_id = db.child('devices').push(device_data)
                device_data['id'] = device_id['name']
                create_qrcode(device_data, f"{device_data['name']} {device_data['id']}", 'device', qr_save_path)

            else:
                line_count = 1


def device_list():
    all_devices = db.child("devices").get().val()
    if all_devices:
        all_devices = dict(all_devices)
        all_devices_list = []
        for key, val in all_devices.items():
            val = dict(val)
            single_device = [key]
            for item_key, item_val in val.items():
                single_device.append(item_val)
            all_devices_list.append(single_device)
        if any(all_devices_list):
            return all_devices_list, True
    else:
        return [[]], False


def remove_device_from_database(user):
    pass


def read_device_list(user):
    pass


def read_device(user):
    pass


def update_device(user):
    pass


def user_log_in(email: str, password: str) -> None:
    user, msg = None, "successful"
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        # print(user)
        with open(path.join('../security', "auth.json"), "w") as outfile:
            json.dump(user, outfile)

    except requests.exceptions.HTTPError as error:
        # print('Invalid email or password')
        msg = 'Invalid email or password'
    except requests.exceptions.ConnectionError as error:
        # print('Network problem')
        msg = 'Network problem'
    except requests.exceptions.Timeout as error:
        # print('Request times out')
        msg = 'Request times out'
    return user, msg

    # user = auth.refresh(user['refreshToken'])
    # print(user)

if __name__ == '__main__':
    device_list()