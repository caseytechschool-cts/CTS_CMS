from cryptography.fernet import Fernet


def key_generation():
    key = Fernet.generate_key()
    with open('../security/key.key', 'wb') as file:
        file.write(key)
    return key
