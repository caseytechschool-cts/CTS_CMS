import qrcode
from os import path, makedirs
from PIL import Image


def resize_QRcode(file_path, file_name, sub_path):
    dir_path = path.join('../QRCode', sub_path, 'reSized')
    makedirs(dir_path, exist_ok=True)
    image = Image.open(file_path)
    image.thumbnail((100, 100))
    file_name = f"{file_name}_resized.png"
    file_path = path.join(dir_path, file_name)
    image.save(file_path)


def create_qrcode(data, id, sub_path):
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    file_name = f"{id}.png"
    file_path = path.join('../QRCode', sub_path, file_name)
    img.save(file_path)
    resize_QRcode(file_path, id, sub_path)


if __name__ == '__main__':
    data = {
        'id': 0,
        'name': 'SM Abdullah',
        'school': 'Berwick Grammar',
        'role': 'student'
    }
    create_qrcode(data, data['id'], 'staff')
