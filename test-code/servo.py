from gpiozero import AngularServo
import time

servo = AngularServo(5, min_pulse_width=0.0006, max_pulse_width=0.0023)

while True:
    servo.angle = -180
    time.sleep(2)
    servo.angle = 180
    time.sleep(2)
