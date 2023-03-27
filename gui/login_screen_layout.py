import PySimpleGUI as sg
import os


def file_exist(filename, f):
    if os.path.exists(os.path.join('../security', filename)):
        print(filename)
        with open(os.path.join('../security', filename)) as file:
            user_name = f.decrypt(file.read())
            return user_name.decode()
    return ""


def login_screen_layout(f):
    user_name_value = file_exist('uname', f)
    password_value = file_exist('pword', f)
    font_underline = ('Century Gothic', 10, 'underline')
    font_normal = ('Century Gothic', 10, '')
    login_screen_components = [
        [sg.Push(background_color='white'),
         sg.Text(text='Login to CTS CMS', background_color='white', font=('Century Gothic', 16, ''),
                 pad=((10, 10), (20, 10))),
         sg.Push(background_color='white')],
        [sg.Text(text='Email:', background_color='white', font=font_normal, pad=((10, 10), (10, 0)))],
        [sg.Input(key='-username-', background_color='#f5f7fb', font=font_normal, pad=((10, 10), (10, 0)),
                  default_text=user_name_value)],
        [sg.Text(text='Password:', background_color='white', font=font_normal, pad=((10, 10), (10, 0)))],
        [sg.Input(key='-password-', password_char='*', background_color='#f5f7fb', font=font_normal, pad=((10, 10), (10, 0)),
                  default_text=password_value)],
        [sg.Checkbox(text='Show Password', key='-show-password-', background_color='white', font=font_normal,
                     pad=((10, 10), (10, 0)), default=False, enable_events=True)],
        [sg.Checkbox(text='Remember me', key='-remember-me-', background_color='white', font=font_normal,
                     pad=((10, 10), (10, 0)), default=False, enable_events=True), sg.Push(background_color='white'),
         sg.Checkbox(text='Forget me', key='-forget-me-', background_color='white', font=font_normal,
                     pad=((10, 10), (10, 0)), default=False, enable_events=True)
         ],
        [sg.Button(button_text='SIGN IN', key='-sign-in-', expand_x=True, font=('Century Gothic', 14, 'bold'), pad=((10, 10), (10, 0)))],
        [sg.Text(text='Forgot Password?', font=font_underline, key='-forgot-', background_color='white',
                 pad=((10, 10), (10, 0)), enable_events=True)],
        [sg.Text(text="Don't have an account? Sign up?", font=font_underline, key='-sign-up-',
                 background_color='white', pad=((10, 10), (10, 20)), enable_events=True)]
    ]

    return login_screen_components


def signup_screen_layout():
    font_normal = ('Century Gothic', 10, '')
    signup_screen_components = [
        [sg.Push(background_color='white'),
         sg.Text(text='Sign up to CTS CMS', background_color='white', font=('Century Gothic', 16, ''),
                 pad=((10, 10), (20, 10))),
         sg.Push(background_color='white')],
        [sg.Text(text='Email:', background_color='white', font=font_normal, pad=((10, 10), (10, 0)))],
        [sg.Input(key='-username-', background_color='#f5f7fb', font=font_normal, pad=((10, 10), (10, 0)))],
        [sg.Text(text='Password:', background_color='white', font=font_normal, pad=((10, 10), (10, 0)))],
        [sg.Input(key='-password-', password_char='*', background_color='#f5f7fb', font=font_normal,
                  pad=((10, 10), (10, 0)))],
        [sg.Button(button_text='SIGN UP NOW', key='-sign-up-now', expand_x=True, font=('Century Gothic', 14, 'bold'),
                   pad=((10, 10), (10, 20)))]
    ]

    return signup_screen_components


def layout_mixer_auth(f):
    return [
        [sg.VPush()],
        [sg.Column(login_screen_layout(f), justification='c', background_color='white', visible=True,
                   key='-login-screen-'),
         sg.Column(signup_screen_layout(), justification='c', background_color='white', visible=False,
                   key='-signup-screen-')],
        [sg.VPush()]
    ]