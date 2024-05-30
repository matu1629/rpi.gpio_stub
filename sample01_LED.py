# base
# https://qiita.com/elyoshio92/items/ccb27786302983cd5057
# reference
# https://raspberrylife.wordpress.com/2013/11/28/dynamic-led/

import RPi.GPIO as GPIO

# GPIO port for the pin
Segments = (11,)

#--------------------------------------------
# switch LED light
#--------------------------------------------
def switchLight(gpio, number):
    if number == 1:
        GPIO.output(gpio, GPIO.HIGH)
    else:
        GPIO.output(gpio, GPIO.LOW)

#--------------------------------------------
# main
# this program light a LED
#--------------------------------------------
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    for s in Segments:
        GPIO.setup(s, GPIO.OUT)
        GPIO.output(s, GPIO.LOW)
    try:
        switchLight(Segments[0], 1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        GPIO.cleanup()