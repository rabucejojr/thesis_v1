from gpiozero import AngularServo
import time

servo = AngularServo(17,min_angle=-180,max_angle=180)

while True:
    servo.angle = -180
    time.sleep(2)
    servo.angle = 180
    time.sleep(2)
