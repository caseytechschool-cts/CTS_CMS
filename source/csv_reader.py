import csv
from os import path, makedirs
import uuid
from qrcode_generator import create_qrcode
from qrcode_reader import read_qrcode_from_path


def csv_student_reader(filename: str) -> None:
    filepath = path.join('../CSV', filename)
    makedirs(path.join('../QRCode', 'school'), exist_ok=True)
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
                create_qrcode(student, student['id'], 'school')
            else:
                line_count += 1


if __name__ == '__main__':
    csv_student_reader('booking.csv')
    read_qrcode_from_path('school')  # 'device'
