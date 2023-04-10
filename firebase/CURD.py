from os import path, makedirs
import requests
import csv
import json
from firebase.config import *
from qr_code.qrcode_generator import create_qrcode
from pathlib import Path


def add_device_to_database(window, csv_files, idToken):
    csv_file_paths = csv_files.split(';')
    for dir_path in csv_file_paths:
        with open(dir_path) as devices:
            csv_data = csv.reader(devices)
            line_count = 0
            all_rows = []
            for row in csv_data:
                if line_count:
                    device_data = {
                        "name": row[0],
                        "device_type": row[1],
                        "device_sub_type": row[2],
                        "isFaulty": False,
                        "location": row[3]
                    }
                    device_id = db.child('devices').push(device_data, token=idToken)
                    row.append(str(device_id['name']))
                else:
                    line_count = 1
                    row.append('device_id')
                all_rows.append(row)
        with open(dir_path, 'w', newline='') as csv_device:
            writer = csv.writer(csv_device)
            writer.writerows(all_rows)
    window.write_event_value('-Thread-device-upload-', 'done')


def device_list(idToken):
    all_devices = db.child("devices").get(token=idToken).val()
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
        return [], False


def remove_device_from_database(device_id, idToken):
    db.child('devices').child(device_id).remove(token=idToken)


def user_log_in(email: str, password: str) -> None:
    user, msg = None, "successful"
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        # print(user)
        with open(path.join('../firebase', "auth.json"), "w") as outfile:
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


if __name__ == '__main__':
    device_list()
