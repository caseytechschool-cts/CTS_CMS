import qrcode
from os import path
from PIL import Image


def resize_QRcode(file_path, file_name):
    image = Image.open(file_path)
    image.thumbnail((100, 100))
    file_name = f"{file_name}_resized.png"
    file_path = path.join('../QRCode/resized', file_name)
    image.save(file_path)


def create_qrcode(data):
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    file_name = f"{data['id']}.png"
    file_path = path.join('../QRCode', file_name)
    img.save(file_path)
    resize_QRcode(file_path, data['id'])


if __name__ == '__main__':
    data = {
        'id': 0,
        'name': 'SM Abdullah',
        'school': 'Berwick Grammar',
        'role': 'student',
        'isBorrower': False
    }
    create_qrcode(data)
