import csv
from os import path, makedirs
import uuid
from qr_code.qrcode_generator import create_qrcode
from pathlib import Path

def csv_student_reader(window, filename: str, default=True) -> None:
    if default:
        filepath = path.join('../CSV', filename)
        qr_save_path = path.join('../QRCode', 'school')
        makedirs(qr_save_path, exist_ok=True)
    else:
        filepath = filename
        qr_save_path = path.join(Path.home(), 'Downloads', 'Student QRCode')
        makedirs(qr_save_path, exist_ok=True)
    with open(filepath) as file:
        csv_data = csv.reader(file)
        line_count = 0
        for row in csv_data:
            if line_count:
                student = {
                    "id": str(uuid.uuid4()),
                    "email": row[0],
                    "first_name": row[1],
                    "last_name": row[2],
                    "preferred_name": row[3],
                    "role": row[4]
                }
                qr_file_name = f"{student['first_name']} {student['last_name']} {student['id']}"
                create_qrcode(student, qr_file_name, 'school', qr_save_path)
            else:
                line_count += 1
    window.write_event_value('-Thread-student-qrcode-', 'done')


# if __name__ == '__main__':
#     csv_student_reader('booking.csv')
#     read_qrcode_from_path('school')  # 'device'
