import PySimpleGUI as sg
import login_screen_layout
from helper_lib.base64image import image_to_base64
from security import generate_key
from pathlib import Path
from cryptography.fernet import Fernet
import os


def show_main_screen():
    sg.theme('Material1')
    key_path = Path(os.path.join('../security', 'key.key'))
    if key_path.is_file():
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
    else:
        key = generate_key.key_generation()
    f = Fernet(key)
    window_login_in = sg.Window(title="Login screen",
                                layout=login_screen_layout.layout_mixer_auth(f),
                                size=(800, 600),
                                margins=(20, 20),
                                icon=image_to_base64('logo.png'),
                                alpha_channel=1.0,
                                finalize=True)

    while True:
        event, values = window_login_in.read(timeout=100)
        print(event)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if values['-show-password-']:
            window_login_in['-password-'].update(password_char='')
        else:
            window_login_in['-password-'].update(password_char='*')
        if event == '-sign-in-':
            if values['-remember-me-']:
                with open('../security/uname', 'wb') as username:
                    user_name = f.encrypt(bytes(values['-username-'], encoding='utf8'))
                    username.write(user_name)
                with open('../security/pword', 'wb') as userpass:
                    password = f.encrypt(bytes(values['-password-'], encoding='utf8'))
                    userpass.write(password)
            if values['-forget-me-']:
                if os.path.exists(os.path.join('../security', 'uname')):
                    os.remove(os.path.join('../security', 'uname'))
                if os.path.exists(os.path.join('../security', 'pword')):
                    os.remove(os.path.join('../security', 'pword'))
        if event == '-sign-up-':
            window_login_in['-login-screen-'].update(visible=False)
            window_login_in['-signup-screen-'].update(visible=True)
            window_login_in.set_title('Sign up page')
        if event == '-sign-up-now':
            window_login_in['-login-screen-'].update(visible=True)
            window_login_in['-signup-screen-'].update(visible=False)
            window_login_in.set_title('Login page')


if __name__ == '__main__':
    show_main_screen()
