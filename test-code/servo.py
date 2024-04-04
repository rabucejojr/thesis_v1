import RPi.GPIO as GPIO
from time import sleep

servo1 = 29
servo2 = 31
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo1, GPIO.OUT)
GPIO.setup(servo2, GPIO.OUT)
p1 = GPIO.PWM(servo1, 50) 
p2 = GPIO.PWM(servo2, 50)# GPIO 17 for PWM with 50Hz
p.start(2.5)  # Initialization
try:
    while True:
        p1.ChangeDutyCycle(5)
        p2.ChangeDutyCycle(5)
        sleep(0.5)
        p1.ChangeDutyCycle(7.5)
        p2.ChangeDutyCycle(7.5)
        sleep(0.5)
        p1.ChangeDutyCycle(10)
        p2.ChangeDutyCycle(10)
        sleep(0.5)
        p1.ChangeDutyCycle(12.5)
        p2.ChangeDutyCycle(12.5)
        sleep(0.5)

except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
