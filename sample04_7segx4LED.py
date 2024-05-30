# base
# https://qiita.com/elyoshio92/items/ccb27786302983cd5057
# reference
# https://raspberrylife.wordpress.com/2013/11/28/dynamic-led/
# anode common type

import RPi.GPIO as GPIO
import time

INTERVAL = 0.05

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

# GPIO ports for the digit 0-3 pins
Digits = (22,27,17,24)

#--------------------------------------------
# get now time
#--------------------------------------------
def getTime():
    # now time
    n = time.strftime('%H') + time.strftime('%M')
    timeList = list(n)
    return timeList

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
def lightNumber(number, cnt):
    for i in range(0,8):
        switchLight(Segments[i],Num[number][i])

    switchLight(Digits[cnt-1],1) # off
    switchLight(Digits[cnt],0) # on

#--------------------------------------------
# main
# this program display time(HHmm)
#--------------------------------------------
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    for s in Segments:
        GPIO.setup(s, GPIO.OUT)
        GPIO.output(s, GPIO.LOW)
    for d in Digits:
        GPIO.setup(d, GPIO.OUT)
        GPIO.output(d, GPIO.HIGH)
    try:
        # display to time Number
        while True:
            # now time
            lst = getTime()

            # counter reset
            count = 0

            # set display Numbers
            for nm in lst:
                lightNumber(nm, count)
                count+=1
                time.sleep(INTERVAL)
            #break
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        GPIO.cleanup()