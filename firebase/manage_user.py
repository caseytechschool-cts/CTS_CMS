from firebase.config import *


def create_user(email:str, password:str) -> None:
    auth.create_user_with_email_and_password(email, password)


def send_verification_emil():
    pass


def password_reset():
    pass


def delete_user():
    pass