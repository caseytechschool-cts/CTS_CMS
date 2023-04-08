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
        for _ in csv_data:
            if line_count:
                student = {
                    "id": str(uuid.uuid4()),
                }
                qr_file_name = f"qrcode_{count}"
                create_qrcode(student, qr_file_name, qr_code_path)
                count += 1
            else:
                line_count += 1
