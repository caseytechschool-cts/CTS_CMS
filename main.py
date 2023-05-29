import PyPDF2
import json
import PySimpleGUI as sg
from gui import login_screen_layout
from helper_lib.base64image import image_to_base64
from helper_lib.pathmaker import resource_path
from security import generate_key
from cryptography.fernet import Fernet
import os
from firebase import user_log_in
from firebase.manage_user import password_reset, create_user
from gui import show_device_list
from constant.global_info import *
import webbrowser


def show_main_screen():
    sg.theme('Material1')
    key_path = Path(os.path.join(user_data_location, 'key.key'))
    if key_path.is_file():
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
    else:
        key = generate_key.key_generation()
    f = Fernet(key)

    window_login_in = sg.Window(title="CTS CMS :: login screen",
                                layout=login_screen_layout.layout_mixer_auth(f),
                                size=(800, 600),
                                margins=(20, 20),
                                icon=image_to_base64(resource_path(os.path.join('assets', 'logo.png'))),
                                alpha_channel=1.0,
                                finalize=True,
                                font=font_normal)

    window_login_in['-reset-password-username-'].bind('<Return>', '_Enter')
    window_login_in['-password-'].bind('<Return>', '_Enter')
    while True:
        event, values = window_login_in.read(timeout=100)
        # print(event)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == '-docs-':
            webbrowser.open_new_tab('https://casey-tech-school.gitbook.io/cts_cms/')
        if values['-show-password-']:
            window_login_in['-password-'].update(password_char='')
        else:
            window_login_in['-password-'].update(password_char='*')
        if event == '-sign-in-' or event == '-password-' + '_Enter':
            if values['-remember-me-']:
                with open(os.path.join(user_data_location, 'uname'), 'wb') as username:
                    user_name = f.encrypt(bytes(values['-username-'], encoding='utf8'))
                    username.write(user_name)
                with open(os.path.join(user_data_location, 'pword'), 'wb') as userpass:
                    password = f.encrypt(bytes(values['-password-'], encoding='utf8'))
                    userpass.write(password)
            if values['-forget-me-']:
                if os.path.exists(os.path.join(user_data_location, 'uname')):
                    os.remove(os.path.join(user_data_location, 'uname'))
                if os.path.exists(os.path.join(user_data_location, 'pword')):
                    os.remove(os.path.join(user_data_location, 'pword'))
            if os.path.exists(os.path.join(user_data_location, 'auth.json')):
                user = json.load(open(os.path.join(user_data_location, 'auth.json'), ))
            else:
                user, msg = user_log_in.log_in(values['-username-'], values['-password-'])
            if user is None:
                window_login_in['-login-error-'].update(visible=True, value=msg)
            else:
                window_login_in['-login-error-'].update(visible=False, value='')
                window_login_in.close()
                show_device_list.show_device_list_window(user)
        if event == '-sign-up-':
            window_login_in['-login-screen-'].update(visible=False)
            window_login_in['-signup-screen-'].update(visible=True)
            window_login_in.set_title('CTS CMS :: sign up page')
        if event == '-sign-up-now-':
            create_user(values['-username-signup-'], values['-password-signup-'])
            # print('done')
            window_login_in['-login-screen-'].update(visible=True)
            window_login_in['-signup-screen-'].update(visible=False)

            window_login_in.set_title('CTS CMS :: login page')
        if event == '-forgot-':
            window_login_in['-login-screen-'].update(visible=False)
            window_login_in['-signup-screen-'].update(visible=False)
            window_login_in['-reset-screen-'].update(visible=True)
            window_login_in.set_title('CTS CMS :: reset password page')
        if event == '-reset-password-' or event == '-reset-password-username-' + '_Enter':
            reset_status = password_reset(values['-reset-password-username-'])
            if reset_status:
                window_login_in['-reset-error-'].update(value=reset_status, visible=True)
            else:
                window_login_in['-reset-error-'].update(value="", visible=False)
                window_login_in['-reset-msg-'].update(visible=True)
                window_login_in['-login-redirect-'].update(visible=True)
        if event == '-login-redirect-' or event == '-sign-up-to-log-in-':
            window_login_in['-login-screen-'].update(visible=True)
            window_login_in['-signup-screen-'].update(visible=False)
            window_login_in['-reset-screen-'].update(visible=False)
            window_login_in.set_title('CTS CMS :: login page')

    if os.path.exists(os.path.join(user_data_location, 'auth.json')):
        os.remove(os.path.join(user_data_location, 'auth.json'))
    window_login_in.close()


if __name__ == '__main__':
    show_main_screen()
