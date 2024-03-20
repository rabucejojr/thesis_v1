import time
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1
V_RL = 0.1  # Sensor output voltage in clean air
Sensitivity = 1.0  # Sensor sensitivity in PPM/V


while True:
    value = adc.read_adc(0, gain=GAIN)
    value = value * (4.09 / 32767.0)
    ppm = (value - V_RL) / Sensitivity
    print(value)
    print("Ammonia concentration:", ppm, "PPM")
    time.sleep(1)
