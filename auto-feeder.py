# this will be executed thru cron, with schedules 7AM and 4PM, two servos for feeds and water
# crontab for 7AM activation: 0 7 * * * /home/admin/Desktop/thesis_v1/auto-feeder.py
# crontab for 4PM activation: 0 16 * * * /home/admin/Desktop/thesis_v1/auto-feeder.py

import RPi.GPIO as GPIO
from time import sleep

servo1 = 29
servo2 = 31
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) 
GPIO.setup(servo1, GPIO.OUT)
GPIO.setup(servo2, GPIO.OUT)
p1 = GPIO.PWM(servo1, 50) 
p2 = GPIO.PWM(servo2, 50)
p1.start(0)
p2.start(0)# Initialization
try:
    while True:
        p1.ChangeDutyCycle(2.5)
        p2.ChangeDutyCycle(2.5)
        sleep(10)
        p1.ChangeDutyCycle(12.5)
        p2.ChangeDutyCycle(12.5)
        sleep(10)

except KeyboardInterrupt:
    p1.stop()
    p2.stop()
    GPIO.cleanup()

