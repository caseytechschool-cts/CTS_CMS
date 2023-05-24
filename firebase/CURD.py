import csv
import uuid
from firebase.config import *


def add_device_to_database(window, csv_files, idToken):
    csv_file_paths = csv_files.split(';')
    for dir_path in csv_file_paths:
        with open(dir_path) as devices:
            csv_data = csv.reader(devices)
            line_count = 0
            all_rows = []
            add_device_id = True
            for row in csv_data:
                if line_count:
                    device_data = {
                        "name": row[0],
                        "device_type": row[1],
                        "device_sub_type": row[2],
                        "isFaulty": 'false',
                        "location": row[3],
                        "purpose": row[4]
                    }
                    device_id = str(uuid.uuid4())
                    db.child('devices').child(device_id).set(device_data, token=idToken)
                    # print(type(device_id['name']))
                    if add_device_id:
                        row.append(device_id)
                    else:
                        row[5] = device_id
                else:
                    line_count = 1
                    if 'device_id' in row:
                        add_device_id = False
                    else:
                        row.append('device_id')
                if add_device_id:
                    all_rows.append(row)
        if add_device_id:
            with open(dir_path, 'w', newline='') as csv_device:
                writer = csv.writer(csv_device)
                writer.writerows(all_rows)
    window.write_event_value('-Thread-device-upload-', 'done')


def remove_device_from_database(device_id, idToken):
    db.child('devices').child(device_id).remove(token=idToken)



