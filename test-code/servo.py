import RPi.GPIO as GPIO
from time import sleep

servo1 = 29 # for water
servo2 = 31 # for feeds
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) 
GPIO.setup(servo1, GPIO.OUT)
GPIO.setup(servo2, GPIO.OUT)
p1 = GPIO.PWM(servo1, 50) 
p2 = GPIO.PWM(servo2, 50)# GPIO 17 for PWM with 50Hz
p1.start(0)
p2.start(0)# Initialization
try:
    while True:
        p1.ChangeDutyCycle(2.5)
        p2.ChangeDutyCycle(2.5)
        sleep(4)
        p1.ChangeDutyCycle(12.5)
        p2.ChangeDutyCycle(12.5)
        sleep(4)

except KeyboardInterrupt:
    p1.stop()
    p2.stop()
    GPIO.cleanup()
