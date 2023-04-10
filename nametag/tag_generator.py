from pathlib import Path
from os import path, makedirs
import shutil
from nametag.nametags import nametag_image, devicetag_image
from nametag.doc_template import create_doc_with_name_tags
from csv_files import csv_reader


def generate_name_tags(files, destination_folder, show_qr_code, show_box, window):
    csv_file_paths = files.split(';')
    if destination_folder == '':
        destination_folder = path.join(Path.home(), 'Downloads')

    save_in_folder = path.join(destination_folder, 'Name tags')
    if path.exists(save_in_folder):
        shutil.rmtree(save_in_folder)
    makedirs(save_in_folder)

    for csv_file in csv_file_paths:
        if show_qr_code:
            csv_reader.csv_student_reader(csv_file, save_in_folder)
        nametag_image(csv_file, save_in_folder, show_qr_code, show_box)
        create_doc_with_name_tags(save_in_folder)

    window.write_event_value('-thread-name-tags-', 'generated')


def generate_device_tags(files, destination_folder, show_name, window):
    csv_file_paths = files.split(';')
    if destination_folder == '':
        destination_folder = path.join(Path.home(), 'Downloads')

    save_in_folder = path.join(destination_folder, 'Device tags')
    if path.exists(save_in_folder):
        shutil.rmtree(save_in_folder)
    makedirs(save_in_folder)

    for csv_file in csv_file_paths:
        csv_reader.csv_device_reader(csv_file, save_in_folder)
        devicetag_image(csv_file, save_in_folder, show_name)
        create_doc_with_name_tags(save_in_folder)

    window.write_event_value('-thread-device-tags-', 'generated')



