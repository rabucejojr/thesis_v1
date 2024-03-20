import time
import Adafruit_ADS1x15

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
GAIN = 1


def read_analog():
    sensor_value = 0
    for x in range(500):
        # Read the ADC channel 0 value.
        value = adc.read_adc(0, gain=GAIN)
        sensor_value += value  # accumulate readings 500 times
    sensor_value /= 500.0  # take average of readings
    sensor_volt = sensor_value * (4.09 / 32767.0)  # convert average to voltage
    RS_air = ((4.09 * 10.0) / sensor_volt) - 10.0  # calculate RS in fresh air
    R0 = RS_air / 3.6  # calculate R0
    return R0


try:
    while True:
        R0_value = read_analog()
        print("R0 =", R0_value)
        time.sleep(0.5)  # wait 1 second

except KeyboardInterrupt:
    pass
