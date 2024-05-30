# base
# https://qiita.com/elyoshio92/items/ccb27786302983cd5057
# reference
# https://raspberrylife.wordpress.com/2013/11/28/dynamic-led/

from RPi.GPIO.Client import output
import RPi.GPIO as GPIO
import time

# GPIO ports for the 7seg pins
Segments = (11,4,23,8,7,10,18,25)

# Number light pattern
Num = {
    ' ':(0,0,0,0,0,0,0,0),
    '.':(0,0,0,0,0,0,0,1),
    '-':(0,0,0,0,0,0,1,0),
    '0':(1,1,1,1,1,1,0,0),
    '1':(0,1,1,0,0,0,0,0),
    '2':(1,1,0,1,1,0,1,0),
    '3':(1,1,1,1,0,0,1,0),
    '4':(0,1,1,0,0,1,1,0),
    '5':(1,0,1,1,0,1,1,0),
    '6':(1,0,1,1,1,1,1,0),
    '7':(1,1,1,0,0,0,0,0),
    '8':(1,1,1,1,1,1,1,0),
    '9':(1,1,1,1,0,1,1,0),
    'A':(1,1,1,0,1,1,1,0),
    'B':(0,0,1,1,1,1,1,0), # b
    'C':(1,0,0,1,1,1,0,0),
    'D':(0,1,1,1,1,0,1,0), # d
    'E':(1,0,0,1,1,1,1,0),
    'F':(1,0,0,0,1,1,1,0),
}

#--------------------------------------------
# switch 7seg LED light
#--------------------------------------------
def switchLight(gpio, number):
    if number == 1:
        GPIO.output(gpio, GPIO.HIGH)
    else:
        GPIO.output(gpio, GPIO.LOW)

#--------------------------------------------
# set lighting LED Number
#--------------------------------------------
def lightNumber(number):
    for i in range(0,8):
        switchLight(Segments[i],Num[number][i])

#--------------------------------------------
# main
# this program display charactors( .-0123456789AbCdEF)
#--------------------------------------------
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Segments, GPIO.OUT)
    output_value = [GPIO.LOW] * len(Segments)
    GPIO.output(Segments, output_value)
    try:
        chars = " .-0123456789ABCDEF"
        for c in chars:
            lightNumber(c)
            time.sleep(1)

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        GPIO.cleanup()