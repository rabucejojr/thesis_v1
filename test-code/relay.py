from gpiozero import OutputDevice
from time import sleep

pin1 = 17
pin2 = 22

relay1 = OutputDevice(pin1,active_high=False, initial_value=False)
relay2 = OutputDevice(pin2,active_high=False, initial_value=False)
try:
    while True:
        relay1.on()
        sleep(2)
        relay1.off()
        sleep(2)
        relay2.on()
        sleep(2)
        relay2.off()
        sleep(2)
except KeyboardInterrupt:
    print("Exiting Program")

finally:
    relay1.close()
    relay2.close()