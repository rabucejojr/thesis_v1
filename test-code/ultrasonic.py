from gpiozero import DistanceSensor
from time import sleep

sensor1 = DistanceSensor(6,5)
sensor2 = DistanceSensor(26,16)

while True:
    print('Sensor 1', sensor1.distance * 100, 'cm')
    print('Sensor 2', sensor2.distance * 100, 'cm')
    sleep(5)