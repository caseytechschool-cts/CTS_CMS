import csv
from os import path, makedirs
import uuid
from qr_code.qrcode_generator import create_qrcode
import shutil


def csv_student_reader(filepath, destination_folder):
    qr_code_path = path.join(destination_folder, 'qrcode')
    if path.exists(qr_code_path):
        shutil.rmtree(qr_code_path)
    makedirs(qr_code_path)
    with open(filepath) as file:
        csv_data = csv.reader(file)
        line_count = 0
        count = 1
        all_rows = []
        add_student_id = True
        for row in csv_data:
            if line_count:
                student = {
                    "id": str(uuid.uuid4()),
                    "role": row[4].lower()
                }
                qr_file_name = f"qrcode_{count}"
                create_qrcode(student, qr_file_name, qr_code_path)
                count += 1
                if add_student_id:
                    row.append(student['id'])
            else:
                line_count += 1
                if 'id' in row:
                    add_student_id = False
                else:
                    row.append('id')
            if add_student_id:
                all_rows.append(row)
    if add_student_id:
        with open(filepath, 'w', newline='') as csv_student:
            writer = csv.writer(csv_student)
            writer.writerows(all_rows)


def csv_device_reader(filepath, destination_folder):
    qr_code_path = path.join(destination_folder, 'qrcode')
    if path.exists(qr_code_path):
        shutil.rmtree(qr_code_path)
    makedirs(qr_code_path)
    with open(filepath) as file:
        csv_data = csv.reader(file)
        line_count = 0
        count = 1
        for row in csv_data:
            if line_count:
                device = {
                    "name": row[0],
                    "device_type": row[1],
                    "device_sub_type": row[2],
                    "isFaulty": False,
                    "location": row[3],
                    "id": row[4]
                }
                qr_file_name = f"qrcode_{count}"
                create_qrcode(device, qr_file_name, qr_code_path)
                count += 1
            else:
                line_count += 1
