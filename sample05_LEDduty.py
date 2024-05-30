# base
# https://qiita.com/elyoshio92/items/ccb27786302983cd5057
# reference
# https://raspberrylife.wordpress.com/2013/11/28/dynamic-led/
# https://shizenkarasuzon.hatenablog.com/entry/2019/03/04/002116

import time
import RPi.GPIO as GPIO

# GPIO port for the pin
Segments = (11,)

#--------------------------------------------
# main
# this program light a LED with strength
#--------------------------------------------
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    for s in Segments:
        GPIO.setup(s, GPIO.OUT)

    led1 = GPIO.PWM(Segments[0], 50)
    try:
        led1.start(0)
        for i in range(0,100,5):
            led1.ChangeDutyCycle(i)
            time.sleep(0.2)

        for i in range(100,-1,-5):
            led1.ChangeDutyCycle(i)
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        led1.stop()
        GPIO.cleanup()