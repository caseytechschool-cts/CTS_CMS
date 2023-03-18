import qrcode
from os import path, makedirs
from PIL import Image


def resize_QRcode(file_path: str, file_name: str, sub_path: str) -> None:
    dir_path = path.join('../QRCode', sub_path, 'reSized')
    makedirs(dir_path, exist_ok=True)
    image = Image.open(file_path)
    image.thumbnail((100, 100))
    file_name = f"{file_name}_resized.png"
    file_path = path.join(dir_path, file_name)
    image.save(file_path)


def create_qrcode(csv_data: dict, resource_id: str, sub_path: str) -> None:
    qr = qrcode.QRCode()
    qr.add_data(csv_data)
    qr.make(fit=True)
    img = qr.make_image()
    file_name = f"{resource_id}.png"
    file_path = path.join('../QRCode', sub_path, file_name)
    img.save(file_path)
    resize_QRcode(file_path, resource_id, sub_path)


if __name__ == '__main__':
    data = {
        'id': 0,
        'name': 'SM Abdullah',
        'school': 'Berwick Grammar',
        'role': 'student'
    }
    create_qrcode(data, data['id'], 'staff')
