# base
# https://qiita.com/elyoshio92/items/ccb27786302983cd5057
# reference
# https://raspberrylife.wordpress.com/2013/11/28/dynamic-led/

import RPi.GPIO as GPIO
import time

INTERVAL = 1

# GPIO ports for pins
Segments = (4, 10, 11)

#--------------------------------------------
# switch Color LED light
#--------------------------------------------
def switchLight(gpio, number):
    if number == 1:
        GPIO.output(gpio, GPIO.HIGH)
    else:
        GPIO.output(gpio, GPIO.LOW)

#--------------------------------------------
# main
# this program light a color LED(ref, green, blue, magenta, yellow, cyan, white)
#--------------------------------------------
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    for s in Segments:
        GPIO.setup(s, GPIO.OUT)
        GPIO.output(s, GPIO.LOW)
    try:
        for i in range(0, len(Segments)):
            switchLight(Segments[i], 1)
            time.sleep(INTERVAL)
            switchLight(Segments[i], 0)
            time.sleep(INTERVAL)
        for i in range(0, len(Segments)):
            switchLight(Segments[i], 1)
            switchLight(Segments[i - 1], 1)
            time.sleep(INTERVAL)
            switchLight(Segments[i], 0)
            switchLight(Segments[i - 1], 0)
            time.sleep(INTERVAL)
        switchLight(Segments[0], 1)
        switchLight(Segments[1], 1)
        switchLight(Segments[2], 1)
        time.sleep(INTERVAL)
        switchLight(Segments[0], 0)
        switchLight(Segments[1], 0)
        switchLight(Segments[2], 0)
        time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        GPIO.cleanup()