from firebase.config import *


def create_user(email: str, password: str) -> None:
    auth.create_user_with_email_and_password(email, password)


def send_verification_emil():
    pass


def password_reset(email):
    try:
        auth.send_password_reset_email(email)
        return ""
    except:
        return "Please provide a valid email address"


def delete_user():
    pass
