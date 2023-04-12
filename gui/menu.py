

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
        ['&File', ['Borrowed device list', 'Download device list CSV file template',
                   'Download student booking CSV file template', '---', 'E&xit']],
        ['&Create', ['Student name tag', 'Device QR Code tag']],
        ['Add', ['Devices']],
        ['&Help', ['&About...']],
        ['My account', ['Logout']]
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
