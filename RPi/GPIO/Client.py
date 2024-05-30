from ctypes import Array
import socket
import sys
import io
import time
import select
from typing import Tuple
import COMMON.Telegram as Tel
import COMMON.Common as Cmn

IN = Cmn.IN
OUT = Cmn.OUT
HIGH = Cmn.HIGH
LOW = Cmn.LOW
PUD_OFF = Cmn.PUD_OFF
PUD_DOWN = Cmn.PUD_DOWN
PUD_UP = Cmn.PUD_UP
MODE_UNKNOWN = Cmn.MODE_UNKNOWN
BCM = Cmn.BCM

BCMChannel = range(1, 54) #[1, 53]

def errorExit(msg):
    print(msg)
    sys.exit()

class Stub:
    def __init__(self):
        self.status = [-1] * len(BCMChannel)
        self.mode = MODE_UNKNOWN
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def send(self, channel, value):
        if value != LOW and value != HIGH:
            return
        v = Cmn.HIGH_VALUE
        if value == LOW:
            v = Cmn.LOW_VALUE
        try:
            buffer = io.BytesIO()
            buffer.write(Tel.Telegram(channel, v))
            self.client.sendto(buffer.getvalue(), (Cmn.HOST, Cmn.PORT))
        except Exception as e:
            errorExit(e)

    def recv(self, channel):
        try:
            buffer = io.BytesIO()
            buffer.write(Tel.Telegram(channel, 0))
            self.client.sendto(buffer.getvalue(), (Cmn.HOST, Cmn.PORT))
            readlist, _, _ = select.select([self.client], [], [], 1)
            if len(readlist) == 0:
                errorExit("no response")
            for r in readlist:
                message, addr = self.client.recvfrom(Tel.BUFSIZE)
                buffer = io.BytesIO(message)
                tel = Tel.Telegram()
                buffer.readinto(tel)
                if tel.value == Cmn.LOW_VALUE:
                    return LOW
                return HIGH
        except Exception as e:
            errorExit(e)

    def sendasitis(self, channel, value):
        try:
            buffer = io.BytesIO()
            buffer.write(Tel.Telegram(channel, value))
            self.client.sendto(buffer.getvalue(), (Cmn.HOST, Cmn.PORT))
        except Exception as e:
            errorExit(e)

stub = Stub()

class PWM:
    PWMChannel = []
    def __init__(self, channel, freqency):
        if channel not in BCMChannel:
            errorExit("The channel sent is invalid on a Raspberry Pi")
        if channel in PWM.PWMChannel:
            errorExit("A PWM object already exists for this GPIO channel")
        if stub.status[BCMChannel.index(channel)] != OUT:
            errorExit("You must setup() the GPIO channel as an output first")
        if freqency < 0.0:
            errorExit("frequency must be greater than 0.0")
        self.channel = channel
        self.sleeptime = 1.0 / freqency
        self.run = False
    def start(self, dutyratio):
        if self.run:
            return
        if dutyratio < 0.0 or dutyratio > 100.0:
            errorExit("dutycycle must have a value from 0.0 to 100.0")
        PWM.PWMChannel.append(self.channel)
        self.run = True
        value = Cmn.convertP2V(dutyratio) # alternate duty cilre
        time.sleep(self.sleeptime) # alternate frequency
        stub.sendasitis(self.channel, value)
    def stop(self):
        if not self.run:
            return
        self.run = False
        PWM.PWMChannel.remove(self.channel)
    def ChangeDutyCycle(self, dutyratio):
        if not self.run:
            return
        if dutyratio < 0.0 or dutyratio > 100.0:
            errorExit("dutycycle must have a value from 0.0 to 100.0")
        value = Cmn.convertP2V(dutyratio) # alternate duty cilre
        time.sleep(self.sleeptime) # alternate frequency
        stub.sendasitis(self.channel, value)
    def ChangeFrequency(self, freqency):
        if not self.run:
            return
        if freqency <= 0.0:
            errorExit("frequency must be greater than 0.0")
        self.sleeptime = 1.0 / freqency

def setmode(mode):
    if mode != BCM:
        errorExit("this stub supports only BCM")
    stub.mode = mode

def getmode():
    return stub.mode

def setup(channel, direction, pull_up_down=PUD_OFF, initial=-1):
    def setup_one(channel, direction, pull_up_down=PUD_OFF, initial=-1):
        if channel not in BCMChannel:
            errorExit("The channel sent is invalid on a Raspberry Pi")
        if stub.status[BCMChannel.index(channel)] != -1:
            errorExit("This channel is already in use")
        stub.status[BCMChannel.index(channel)] = direction
        if direction == OUT and (initial == LOW or initial == HIGH):
            output(channel, initial)
    if stub.mode != BCM:
        errorExit("this stub supports only BCM")
    if direction != IN and direction != OUT:
        errorExit("An invalid direction was passed to setup()")
    if direction == OUT and pull_up_down != PUD_OFF:
        errorExit("pull_up_down parameter is not valid for outputs")
    if direction == IN and initial != -1:
        errorExit("initial parameter is not valid for inputs")
    if pull_up_down != PUD_OFF and pull_up_down != PUD_DOWN and pull_up_down != PUD_UP:
        errorExit("Invalid value for pull_up_down - should be either PUD_OFF, PUD_UP or PUD_DOWN")
    if type(channel) is int:
        setup_one(channel, direction, pull_up_down, initial)
    elif type(channel) is list or type(channel) is tuple:
        for c in channel:
            setup_one(c, direction, pull_up_down, initial)
    else:
        errorExit("Channel must be an integer or list/tuple of integers")

def output(channel, value):
    def output_one(channel, value):
        if channel not in BCMChannel:
            errorExit("The channel sent is invalid on a Raspberry Pi")
        if stub.status[BCMChannel.index(channel)] != OUT:
            errorExit("The GPIO channel has not been set up as an OUTPUT")
        if value != LOW and value != HIGH:
            errorExit("this stub suports HIGH or LOW")
        stub.send(channel, value)
    if type(channel) is int and type(value) is int:
        output_one(channel, value)
    elif (type(channel) is list or type(channel) is tuple) and (type(value) is list or type(value) is tuple):
        if len(channel) != len(value):
            errorExit("Number of channels != number of values")
        for (c, v) in zip(channel, value):
            output_one(c, v)
    else:
        errorExit("Channel and Value must be an integer or list/tuple of integers")

def input(channel):
    if channel not in BCMChannel:
        errorExit("The channel sent is invalid on a Raspberry Pi")
    if stub.status[BCMChannel.index(channel)] != IN and stub.status[BCMChannel.index(channel)] != OUT:
        errorExit("You must setup() the GPIO channel first")
    return stub.recv(channel)

def cleanup():
    time.sleep(0.1)
    stub.sendasitis(0, 0) # off
    stub.client.close()
