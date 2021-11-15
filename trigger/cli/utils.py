#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import os


TRUE_BOOLEAN = ("YES", "Y")
FALSE_BOOLEAN = ("NO", "N")


def get_prog():
    return 'trigger'


def get_terminal_size():
    """Returns a tuple (x, y) representing the width(x) and the height(x)
    in characters of the terminal window."""

    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            import struct

            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
                                                 '1234'))
        except:
            return None
        if cr == (0, 0):
            return None
        if cr == (0, 0):
            return None
        return cr

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (os.environ.get('LINES', 25), os.environ.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])


def get_userinput_boolean(msg, retry=3):
    for i in range(retry):
        resp = input(msg)
        if resp.upper() in TRUE_BOOLEAN + FALSE_BOOLEAN:
            break
    else:
        sys.stderr.write("The pagrant could been created due to the user's wrong input\n")
        sys.exit(1)
    return resp


def get_userinput_str(msg, retry=3):
    for i in range(3):
        resp = input(msg)
        if not resp or len(resp) == 0:
            continue
        return resp


def get_userinput_int(msg, retry=3):
    for i in range(3):
        resp = input(msg)
        try:
            int_resp = int(resp)
            return int_resp
        except ValueError:
            continue


def get_userinput_choice(choice_list, message, retry=3):
    choice_message_list = ["%s : %s " % (i + 1, v) for i, v in enumerate(choice_list)]
    msg_list = [message]
    msg_list.extend(choice_message_list)
    msg_list.append("Your choose is : ")
    for i in range(3):
        resp = input("\n".join(msg_list))
        try:
            int_resp = int(resp)
            if int_resp < 1 or int_resp > len(choice_list):
                return
            return choice_list[int_resp - 1]
        except ValueError:
            continue


def is_true(value):
    return value.upper() in TRUE_BOOLEAN
