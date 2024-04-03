from gpiozero.pins.pigpio import PiGPIOFactory

from gpiozero import Servo
from time import sleep

# create a custom pin-factory to fix servo jitter
# more info here: https://gpiozero.readthedocs.io/en/stable/api_output.html#servo
# and here: https://gpiozero.readthedocs.io/en/stable/api_pins.html
pigpio_factory = PiGPIOFactory()

servo = Servo(22, pin_factory=pigpio_factory)
servo.mid()
print("servo mid")
sleep(3)

while True:
  servo.min()
  print("servo min")
  sleep(3)

  servo.mid()
  print("servo mid")  
  sleep(3)

  servo.max()
  print("servo max")
  sleep(3)