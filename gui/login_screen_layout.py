import PySimpleGUI as sg
import os
import json
from constant.global_info import *


def file_exist(filename, f=None):
    if os.path.exists(os.path.join(user_data_location, filename)):
        with open(os.path.join(user_data_location, filename)) as file:
            user_name = f.decrypt(file.read())
            return user_name.decode()
    return ""


def login_screen_layout(f):
    user_name_value = file_exist('uname', f=f)
    password_value = file_exist('pword', f=f)

    if os.path.exists(os.path.join(user_data_location, 'auth.json')):
        json_email = json.load(open(os.path.join(user_data_location, 'auth.json')))
        user_name_value = json_email['email']

    login_screen_components = [
        [sg.Push(background_color='white'),
         sg.Text(text='Login to CTS CMS', background_color='white', font=font_heading,
                 pad=((10, 10), (20, 10))), sg.Push(background_color='white')],
        [sg.Text(text='', background_color='white', font=font_normal,
                 pad=((10, 10), (10, 0)), key='-login-error-', text_color='red', visible=False)],
        [sg.Text(text='Email:', background_color='white', font=font_normal, pad=((10, 10), (10, 0)))],
        [sg.Input(key='-username-', background_color='#f5f7fb', font=font_normal, pad=((10, 10), (10, 0)),
                  default_text=user_name_value)],
        [sg.Text(text='Password:', background_color='white', font=font_normal, pad=((10, 10), (10, 0)))],
        [sg.Input(key='-password-', password_char='*', background_color='#f5f7fb', font=font_normal,
                  pad=((10, 10), (10, 0)), default_text=password_value)],
        [sg.Checkbox(text='Show Password', key='-show-password-', background_color='white', font=font_normal,
                     pad=((10, 10), (10, 0)), default=False, enable_events=True)],
        [sg.Checkbox(text='Remember me', key='-remember-me-', background_color='white', font=font_normal,
                     pad=((10, 10), (10, 0)), default=False, enable_events=True), sg.Push(background_color='white'),
         sg.Checkbox(text='Forget me', key='-forget-me-', background_color='white', font=font_normal,
                     pad=((10, 10), (10, 0)), default=False, enable_events=True)
         ],
        [sg.Button(button_text='SIGN IN NOW', key='-sign-in-', expand_x=True, font=account_button_font,
                   pad=((10, 10), (20, 0)))],
        [sg.Text(text='Forgot Password?', font=font_underline, key='-forgot-', background_color='white',
                 pad=((10, 10), (10, 0)), enable_events=True)],
        [sg.Text(text="Don't have an account? Sign up?", font=font_underline, key='-sign-up-',
                 background_color='white', pad=((10, 10), (10, 20)), enable_events=True)]
    ]

    return login_screen_components


def signup_screen_layout():
    signup_screen_components = [
        [sg.Push(background_color='white'),
         sg.Text(text='Sign up to CTS CMS', background_color='white', font=font_heading, pad=((10, 10), (20, 10))),
         sg.Push(background_color='white')],
        [sg.Text(text='Email:', background_color='white', font=font_normal, pad=((10, 10), (10, 0)))],
        [sg.Input(key='-username-signup-', background_color='#f5f7fb', font=font_normal, pad=((10, 10), (10, 0)))],
        [sg.Text(text='Password:', background_color='white', font=font_normal, pad=((10, 10), (10, 0)))],
        [sg.Input(key='-password-signup-', password_char='*', background_color='#f5f7fb', font=font_normal,
                  pad=((10, 10), (10, 0)))],
        [sg.Button(button_text='SIGN UP NOW', key='-sign-up-now-', expand_x=True, font=account_button_font,
                   pad=((10, 10), (20, 20)))],
        [sg.Text(text='Already have an account? Login here', font=font_underline, background_color='white',
                 pad=((10, 10), (10, 20)), key='-sign-up-to-log-in-', enable_events=True)]
    ]

    return signup_screen_components


def reset_password_function():
    reset_password_components = [
        [sg.Push(background_color='white'), sg.Text(text='Reset password', background_color='white',
                                                    font=font_heading, pad=((10, 10), (20, 10))),
         sg.Push(background_color='white')],
        [sg.Text(text='', background_color='white', font=font_normal,
                 pad=((10, 10), (10, 0)), key='-reset-error-', text_color='red', visible=False)],
        [sg.Text(text='Email:', background_color='white', font=font_normal, pad=((10, 10), (10, 0)))],
        [sg.Input(key='-reset-password-username-', background_color='#f5f7fb', font=font_normal,
                  pad=((10, 10), (10, 0)), do_not_clear=False)],
        [sg.Button(button_text='Reset password', key='-reset-password-', expand_x=True,
                   font=account_button_font, pad=((10, 10), (20, 20)))],
        [sg.Text(text='Check your email for the reset link', background_color='white', visible=False,
                 pad=((10, 10), (10, 10)), key='-reset-msg-', font=font_normal)],
        [sg.Text(text='Jump to the login page', background_color='white', visible=False, enable_events=True,
                 pad=((10, 10), (0, 20)), key='-login-redirect-', font=font_underline)]
    ]
    return reset_password_components


def layout_mixer_auth(f):
    return [
        [sg.VPush()],
        [sg.Column(login_screen_layout(f), justification='c', background_color='white', visible=True,
                   key='-login-screen-'),
         sg.Column(signup_screen_layout(), justification='c', background_color='white', visible=False,
                   key='-signup-screen-'),
         sg.Column(reset_password_function(), justification='c', background_color='white', visible=False,
                   key='-reset-screen-')
         ],
        [sg.VPush()]
    ]
