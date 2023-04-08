from pathlib import Path
from os import path, makedirs
import shutil

import nametag.nametags
from csv_files import csv_reader


def generate_name_tags(files, destination_folder, show_qr_code, show_box):
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
        nametag.nametags.nametag_image(csv_file, save_in_folder, show_qr_code, show_box)

