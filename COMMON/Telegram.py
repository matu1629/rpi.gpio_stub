from ctypes import *
BUFSIZE = 4

class Telegram(Structure):
    _fields_ = (
        ("channel", c_uint16),
        ("value", c_uint16),
    )
