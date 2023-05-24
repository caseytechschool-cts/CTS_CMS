from firebase.config import *
import os.path
import json
import requests
from constant.global_info import user_data_location


def log_in(email: str, password: str):
    user, msg = None, "successful"
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        with open(os.path.join(user_data_location, "auth.json"), "w") as outfile:
            json.dump(user, outfile)

    except requests.exceptions.HTTPError as error:
        msg = 'Invalid email or password'
    except requests.exceptions.ConnectionError as error:
        msg = 'Network problem'
    except requests.exceptions.Timeout as error:
        msg = 'Request times out'
    return user, msg
