# base
# https://qiita.com/elyoshio92/items/ccb27786302983cd5057
# reference
# https://raspberrylife.wordpress.com/2013/11/28/dynamic-led/
# https://shizenkarasuzon.hatenablog.com/entry/2019/03/04/002116
# FEETEC Servo FS90

import time
import RPi.GPIO as GPIO

# GPIO port for the pin
Segments = (11,)

#--------------------------------------------
# main
# this program move a servo(-90, 90, -45, 45, 0, -90, 90)
#--------------------------------------------
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    for s in Segments:
        GPIO.setup(s, GPIO.OUT)

    servo = GPIO.PWM(Segments[0], 50)
    try:
        servo.start(2.5)
        time.sleep(1)
        servo.ChangeDutyCycle(12.5)
        time.sleep(1)
        servo.ChangeDutyCycle(5)
        time.sleep(1)
        servo.ChangeDutyCycle(10)
        time.sleep(1)
        servo.ChangeDutyCycle(7.5)
        time.sleep(1)
        servo.ChangeDutyCycle(2.5)
        time.sleep(1)
        servo.ChangeDutyCycle(12.5)
        time.sleep(1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        servo.stop()
        GPIO.cleanup()