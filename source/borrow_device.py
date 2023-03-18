from qrcode_reader import read_qrcode_from_webcam
from config import *


def borrow_item() -> None:
    """ This function triggers when a student borrow a device. It gets the student_id and device_data and stores the
    information in the firebase database

    :return: None
    """
    # try:
    #     # student_id = scan_student_qrcode()
    #     # device_data = scan_device_qrcode()
    #     # db.child('devices').child(device_data['id']).update({'borrowed_by': student_id})
    #     # db.child('borrowed_devices').child(device_data['id']).set({'student_id': student_id})
    #     print('Successful')
    # except:
    #     print('Unsuccessful')
    # finally:
    #     print('Return to the main window')

    # testing code. Remove those
    db.child('devices').child('-NQngEuLM4ulrcaFuzF_').update({'borrowed_by': 'Student 1'})
    db.child('borrowed_devices').child('Student 1').set({'device_id': '-NQngEuLM4ulrcaFuzF_'})

    db.child('devices').child('-NQngF1p-TzSDjctZLj-').update({'borrowed_by': 'Student 2'})
    db.child('borrowed_devices').child('Student 2').set({'device_id': '-NQngF1p-TzSDjctZLj-'})

    db.child('devices').child('-NQngFBgNFyDZ-WCQuDj').update({'borrowed_by': 'Student 3'})
    db.child('borrowed_devices').child('Student 3').set({'device_id': '-NQngFBgNFyDZ-WCQuDj'})

    db.child('devices').child('-NQngFL_vJQIUceT1FUR').update({'borrowed_by': 'Student 4'})
    db.child('borrowed_devices').child('Student 4').set({'device_id': '-NQngFL_vJQIUceT1FUR'})

    db.child('devices').child('-NQngFVPS6wWhw67EsD5').update({'borrowed_by': 'Student 5'})
    db.child('borrowed_devices').child('Student 5').set({'device_id': '-NQngFVPS6wWhw67EsD5'})
    # db.child('borrowed_devices').child('siffat').update({'device_id': '-MQIdTRxxoBs0bun9Yrq'})


def scan_student_qrcode() -> str:
    student_qr_data = read_qrcode_from_webcam()
    return student_qr_data['id']


def scan_device_qrcode() -> dict:
    device_qr_data = read_qrcode_from_webcam()
    return device_qr_data


def borrowed_devices_list():
    devices_list = db.child('borrowed_devices').get().val()
    devices_list = dict(devices_list)

    borrowed_device_table_data = []
    for key, value in devices_list.items():
        borrowed_device_table_data.append([key, value['device_id']])

    return borrowed_device_table_data


if __name__ == '__main__':
    print(borrowed_devices_list())
