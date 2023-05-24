from cryptography.fernet import Fernet
from os import path, mkdir
from pathlib import Path


def key_generation():
    if not path.exists(path.join(Path.home(), 'Documents', 'CTS-CMS')):
        mkdir(path.join(Path.home(), 'Documents', 'CTS-CMS'))
    key = Fernet.generate_key()
    with open(path.join(Path.home(), 'Documents', 'CTS-CMS', 'key.key'), 'wb') as file:
        file.write(key)
    return key
