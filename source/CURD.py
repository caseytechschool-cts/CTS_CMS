from os import path, makedirs
import requests
import csv
import json
from source.config import *
import qrcode_generator
from pathmaker import resource_path


def add_device_to_database(filename: str) -> None:
    json_object = None
    try:
        with open(resource_path('auth.json'), 'r') as openfile:
            json_object = json.load(openfile)
    except FileNotFoundError:
        print('Please login to add data')
    if json_object and json_object['localId']:
        with open(path.join('../CSV', filename)) as devices:
            makedirs(path.join('../QRCode', 'device'), exist_ok=True)
            csv_data = csv.reader(devices)
            line_count = 0
            for row in csv_data:
                if line_count:
                    device_data = {
                        "name": row[0],
                        "device_type": row[1],
                        "device_sub_type": row[2],
                        "borrowed_by": "X",
                        "isFaulty": False
                    }
                    device_id = db.child('devices').push(device_data)
                    device_data['id'] = device_id['name']
                    qrcode_generator.create_qrcode(device_data, device_id['name'], 'device')

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


def user_log_in(email: str, password: str) -> None:
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print(user)
        with open("auth.json", "w") as outfile:
            json.dump(user, outfile)

    except requests.exceptions.HTTPError as error:
        print('Invalid email or password')
    except requests.exceptions.ConnectionError as error:
        print('Network problem')
    except requests.exceptions.Timeout as error:
        print('Request times out')

    # user = auth.refresh(user['refreshToken'])
    # print(user)
