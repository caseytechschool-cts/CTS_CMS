from borrow_device import scan_device_qrcode
from config import *


def return_item() -> None:
    device_data = scan_device_qrcode()
    db.child('devices').child(device_data['id']).update({'borrowed_by': 'X'})
    db.child('borrowed_devices').child(device_data['id']).remove()

