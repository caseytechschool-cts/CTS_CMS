import PySimpleGUI as sg


def default_menu():
    """ The default menu without login into the system """
    menu_default = [
        ['&File', ['Show device list', 'Show faulty device list', '---', 'E&xit']],
        ['!&Admin', ['&Create user', '&Remove user', '&Update user']],
        ['!&Generate', ['Student QR code', 'Device QR code', ['Single device', 'Multiple devices']]],
        ['!&Report', ['Faulty device']],
        ['&Help', ['&About...']],
        ['&Login', ['Login']],
        ['!Log&out', ['Logout']]
    ]
    return menu_default


def login_menu():
    menu_login = [
        ['&File', ['Show faulty device list', '---', 'E&xit']],
        ['&Admin', ['&Create users', '&List all users']],
        ['&Create', ['Student QR code']],
        ['Add', ['Devices']],
        ['&Report', ['Faulty device']],
        ['&Help', ['&About...']],
        ['My account', ['Update password', 'Logout']]
    ]
    return menu_login


def super_user_menu_login():
    menu_super_user_login = [
        ['&File', ['Show device list', 'Show faulty device list', '---', 'E&xit']],
        ['&Admin', ['&Create user', '&Remove user', '&Update user']],
        ['&Generate', ['Student QR code', 'Device QR code', ['Single device', 'Multiple devices']]],
        ['&Report', ['Faulty device']],
        ['&Help', ['&About...']],
        ['!&Login', ['Login']],
        ['Log&out', ['Logout']]
    ]
    return menu_super_user_login
