from firebase.config import *


def return_item(device_data) -> None:
    db.child('devices').child(device_data['id']).update({'borrowed_by': 'X'})
    db.child('borrowed_devices').child(device_data['id']).remove()

