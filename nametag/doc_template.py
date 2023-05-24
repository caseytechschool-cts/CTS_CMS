from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import glob
from os import path, makedirs
import uuid
import shutil
from docx2pdf import convert
from PyPDF2 import PdfWriter
import sys
from constant.global_info import user_data_location


def create_doc_with_name_tags(folder_path):
    name_tag_image_path = sorted(glob.glob(path.join(folder_path, 'nametag', '*.png')),
                                 key=lambda img_file: path.getmtime(img_file))
    makedirs(path.join(folder_path, 'nametag doc'))

    num_of_passes = 1
    image_start_location = 0
    image_end_location = min(len(name_tag_image_path), 14)
    if len(name_tag_image_path) > 14:
        num_of_passes = len(name_tag_image_path) // 14
        if len(name_tag_image_path) % 14:
            num_of_passes += 1

    for i in range(num_of_passes):
        doc = DocxTemplate(path.join('data', 'template_with_tags.docx'))
        image_list = []
        for j in range(image_start_location, image_end_location):
            image_obj = InlineImage(doc, name_tag_image_path[j], width=Mm(95), height=Mm(35))
            image_list.append(image_obj)

        context = {}
        for j in range(image_end_location - image_start_location):
            context[f'image{j + 1}'] = image_list[j]

        doc.render(context)
        docx_file_name = f'filled_nametag_{i}.docx'
        doc.save(path.join(folder_path, 'nametag doc', docx_file_name))
        image_start_location = image_end_location
        image_end_location = min(len(name_tag_image_path), image_end_location + 14)

    sys.stderr = open(path.join(user_data_location, "consoleoutput.log"), "w")
    convert(path.join(folder_path, 'nametag doc'))

    merger = PdfWriter()

    pdf_file_list = sorted(glob.glob(path.join(folder_path, 'nametag doc', '*.pdf')),
                           key=lambda pdf_file: path.getmtime(pdf_file))

    for file in pdf_file_list:
        with open(file, "rb") as f:
            merger.append(f)

    # write the merged pdf to a new file
    out_pdf_fname = f'nametags_{uuid.uuid4()}.pdf'
    with open(path.join(folder_path, out_pdf_fname), "wb") as f:
        merger.write(f)
    merger.close()

    if path.exists(path.join(folder_path, 'nametag')):
        shutil.rmtree(path.join(folder_path, 'nametag'))
    if path.exists(path.join(folder_path, 'qrcode')):
        shutil.rmtree(path.join(folder_path, 'qrcode'))
    if path.exists(path.join(folder_path, 'nametag doc')):
        shutil.rmtree(path.join(folder_path, 'nametag doc'))


def create_doc_with_device_tags(folder_path):
    device_tag_image_path = sorted(glob.glob(path.join(folder_path, 'devicetag', '*.png')),
                                 key=lambda img_file: path.getmtime(img_file))
    makedirs(path.join(folder_path, 'devicetag doc'))

    num_of_passes = 1
    image_start_location = 0
    image_end_location = min(len(device_tag_image_path), 24)
    if len(device_tag_image_path) > 24:
        num_of_passes = len(device_tag_image_path) // 24
        if len(device_tag_image_path) % 24:
            num_of_passes += 1

    for i in range(num_of_passes):
        doc = DocxTemplate(path.join('data', 'template_device_tags.docx'))
        image_list = []
        for j in range(image_start_location, image_end_location):
            image_obj = InlineImage(doc, device_tag_image_path[j], width=Mm(63.5), height=Mm(33.87))
            image_list.append(image_obj)

        context = {}
        for j in range(image_end_location - image_start_location):
            context[f'image{j + 1}'] = image_list[j]

        doc.render(context)
        docx_file_name = f'filled_devicetag_{i}.docx'
        doc.save(path.join(folder_path, 'devicetag doc', docx_file_name))
        image_start_location = image_end_location
        image_end_location = min(len(device_tag_image_path), image_end_location + 14)

    sys.stderr = open(path.join(user_data_location, "consoleoutput.log"), "w")
    convert(path.join(folder_path, 'devicetag doc'))

    merger = PdfWriter()

    pdf_file_list = sorted(glob.glob(path.join(folder_path, 'devicetag doc', '*.pdf')),
                           key=lambda pdf_file: path.getmtime(pdf_file))

    for file in pdf_file_list:
        with open(file, "rb") as f:
            merger.append(f)

    # write the merged pdf to a new file
    out_pdf_fname = f'devicetags_{uuid.uuid4()}.pdf'
    with open(path.join(folder_path, out_pdf_fname), "wb") as f:
        merger.write(f)
    merger.close()

    if path.exists(path.join(folder_path, 'devicetag')):
        shutil.rmtree(path.join(folder_path, 'devicetag'))
    if path.exists(path.join(folder_path, 'qrcode')):
        shutil.rmtree(path.join(folder_path, 'qrcode'))
    if path.exists(path.join(folder_path, 'devicetag doc')):
        shutil.rmtree(path.join(folder_path, 'devicetag doc'))

