# base
# https://qiita.com/elyoshio92/items/ccb27786302983cd5057
# reference
# https://raspberrylife.wordpress.com/2013/11/28/dynamic-led/

import time
import RPi.GPIO as GPIO

# GPIO port for the pin
Segments = (11,)

#--------------------------------------------
# main
# this program get a state of a switch(off, on)
#--------------------------------------------
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    for s in Segments:
        GPIO.setup(s, GPIO.IN)
    try:
        while True:
            for s in Segments:
                if GPIO.input(s) == GPIO.LOW:
                    print("off")
                else:
                    print("on")
                time.sleep(0.2)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        GPIO.cleanup()