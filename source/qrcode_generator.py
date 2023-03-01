import qrcode
from os import path


def create_qrcode(data):
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    file_name = f"{data['id']}.png"
    file_path = path.join('../QRCode', file_name)
    img.save(file_path)


if __name__ == '__main__':
    data = {
        'id': 0,
        'name': 'SM Abdullah',
        'school': 'Berwick Grammar',
        'role': 'student',
        'isBorrower': False
    }
    create_qrcode(data)
    qr_data = read_qrcode()

