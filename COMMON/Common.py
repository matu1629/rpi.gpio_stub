import math

HIGH = 1
LOW = 0

IN = 1
OUT = 0

PUD_OFF = 0
PUD_DOWN = 1
PUD_UP = 2

MODE_UNKNOWN = -1
BCM = 11

HOST = "localhost"
PORT = 52017

HIGH_VALUE = 20000
LOW_VALUE = 0
BASE_VALUE = 55 # only color

BG_COLOR = "gray8"

def convertP2V(p):
    '''
    for duty cycle
    [0.0, 100.0] % -> conv[0, 20000]
    '''
    return math.floor(p * 200.0)

def getMonoColor(v):
    '''
    for led
    [0, 20000] -> conv[55, 255] -> conv[#373737, #ffffff]
    '''
    c = v // 100 + BASE_VALUE
    return "#{:02x}{:02x}{:02x}".format(c, c, c)

def getFullColor(r, g, b):
    '''
    for led
    ([0, 20000], [0, 20000], [0, 20000]) -> conv([55, 255], [55, 255], [55, 255]) -> conv[#373737, #ffffff]
    '''
    return "#{:02x}{:02x}{:02x}".format(r // 100 + BASE_VALUE, g // 100 + BASE_VALUE, b // 100 + BASE_VALUE)

def getA(value):
    '''
    for FEETEC Servo FS90
    frequency 50 Hz(20 msec=20,000 usec)
    -90 degree = 500 usec
    0 degree = 1,500 usec
    90 degree = 2,500 usec
    [0, 20000] -> cut[500, 2500] -> conv[-1000, 1000] -> conv[-pi / 2, pi / 2]
    '''
    v = value
    if value < 500:
        v = 500
    elif value > 2500:
        v = 2500
    v -= 1500
    return -v * math.pi / 2000.0 # 2000.0 = 90 degree / 1000 / 180

def getD(value):
    '''
    for FEETEC Servo FS90
    to move 180 degree spend 0.36 sec 
    '''
    delta = 0.137
    if value < 0:
        delta = -0.137
    return delta
