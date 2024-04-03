import RPi.GPIO as GPIO
import time

# Set up GPIO
servo_pin = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Create PWM object
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz (20 ms PWM period)

# Start PWM
pwm.start(0)  # Start with 0% duty cycle

def set_angle(angle):
    duty = angle / 18.0 + 2.5  # Convert angle to duty cycle
    pwm.ChangeDutyCycle(duty)

try:
    while True:
        # Rotate from 0 to 180 degrees
        for angle in range(0, 181, 10):
            set_angle(angle)
            time.sleep(0.5)  # Adjust speed of rotation here

        # Rotate from 180 to 0 degrees
        for angle in range(180, -1, -10):
            set_angle(angle)
            time.sleep(0.5)  # Adjust speed of rotation here

except KeyboardInterrupt:
    # Clean up GPIO
    pwm.stop()
    GPIO.cleanup()
