import csv
import uuid
from qrcode_generator import create_qrcode
from qrcode_reader import read_qrcode


def csv_reader():
    with open('../CSV/booking.csv') as booking:
        reader = csv.reader(booking)
        line_count = 0
        for row in reader:
            if line_count:
                data = {
                    "id": str(uuid.uuid4()),
                    "email": row[0],
                    "first_name": row[1],
                    "last_name": row[2],
                    "preferred_name": row[3],
                    "role": row[4],
                    "is_borrowed": False
                }
                create_qrcode(data)
            line_count += 1


if __name__ == '__main__':
    csv_reader()
    read_qrcode()
