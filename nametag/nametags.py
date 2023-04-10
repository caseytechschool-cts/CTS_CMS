from PIL import Image, ImageDraw, ImageFont
from os import path, makedirs
import shutil
import csv
import glob


def nametag_image(csv_file, destination_folder, show_qr_code, show_box):
    nametag_path = path.join(destination_folder, 'nametag')
    if path.exists(nametag_path):
        shutil.rmtree(nametag_path)
    makedirs(nametag_path)

    if show_qr_code:
        img_paths = sorted(glob.glob(path.join(destination_folder, 'qrcode', '*.png')),
                           key=lambda img_file: path.getmtime(img_file))
    with open(csv_file) as file:
        csv_data = csv.reader(file)
        line_count = 0
        count = 1
        for row in csv_data:
            if line_count:
                img = Image.new('RGBA', (360, 130), color=(255, 255, 255, 0))
                name_font = ImageFont.truetype("arial.ttf", 20)
                first_name = row[1][0:14]
                last_name = row[2][0:14]
                draw = ImageDraw.Draw(img)
                if not show_qr_code and not show_box:
                    draw.text((20, 40), first_name, font=name_font, fill=(0, 0, 0))
                    draw.text((20, 70), last_name, font=name_font, fill=(0, 0, 0))
                elif show_qr_code and not show_box:
                    qr_code_path = img_paths.pop(0)
                    img.paste(Image.open(qr_code_path), (20, 20))
                    draw.text((140, 50), first_name, font=name_font, fill=(0, 0, 0))
                    draw.text((140, 80), last_name, font=name_font, fill=(0, 0, 0))
                elif show_box and not show_qr_code:
                    draw.text((20, 40), first_name, font=name_font, fill=(0, 0, 0))
                    draw.text((20, 70), last_name, font=name_font, fill=(0, 0, 0))
                    draw.rectangle((280, 55, 310, 85), outline=(0, 0, 0))
                else:
                    qr_code_path = img_paths.pop(0)
                    img.paste(Image.open(qr_code_path), (20, 20))
                    draw.text((140, 50), first_name, font=name_font, fill=(0, 0, 0))
                    draw.text((140, 80), last_name, font=name_font, fill=(0, 0, 0))
                    draw.rectangle((310, 55, 340, 85), outline=(0, 0, 0))

                image_file_name = f'image{count}.png'
                img.save(path.join(nametag_path, image_file_name))
                count += 1
            else:
                line_count += 1


def devicetag_image(csv_file, destination_folder, show_name):
    nametag_path = path.join(destination_folder, 'devicetag')
    if path.exists(nametag_path):
        shutil.rmtree(nametag_path)
    makedirs(nametag_path)

    img_paths = sorted(glob.glob(path.join(destination_folder, 'qrcode', '*.png')),
                       key=lambda img_file: path.getmtime(img_file))
    with open(csv_file) as file:
        csv_data = csv.reader(file)
        line_count = 0
        count = 1
        name_font = ImageFont.truetype("arial.ttf", 12)
        for row in csv_data:
            if line_count:
                img = Image.new('RGBA', (240, 128), color=(255, 255, 255, 0))
                draw = ImageDraw.Draw(img)
                if show_name:
                    qr_code_path = img_paths.pop(0)
                    img.paste(Image.open(qr_code_path), (20, 14))
                    draw.text((140, 64), row[0], font=name_font, fill=(0, 0, 0))
                else:
                    qr_code_path = img_paths.pop(0)
                    img.paste(Image.open(qr_code_path), (70, 14))

                image_file_name = f'image{count}.png'
                img.save(path.join(nametag_path, image_file_name))
                count += 1
            else:
                line_count += 1

