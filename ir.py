import RPi.GPIO as GPIO
import time

ir_pin = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(ir_pin, GPIO.IN)

try:
    while True:
        ir_state=GPIO.input(ir_pin)
        print('IR STATE:',ir_state)
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()