

import time
import math
import Adafruit_ADS1x15

# ADC Configuration
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

# MQ Sensor Constants
RL = 47  # The value of resistor RL is 47K
m = -0.263  # Enter calculated Slope
b = 0.42  # Enter calculated intercept
Ro = 20  # Enter found Ro value
MQ_sensor = 0  # Sensor is connected to A0 on ADS1115

def get_ppm(VRL):
    Rs = ((5.0 * RL) / VRL) - RL  # Calculate Rs value
    ratio = Rs / Ro  # Calculate ratio Rs/Ro
    ppm = pow(10, ((math.log10(ratio) - b) / m))  # Calculate ppm
    return ppm

def main():
    print('NH3 in PPM')
    print('-' * 20)

    try:
        while True:
            # Read analog voltage from MQ sensor
            value = adc.read_adc(MQ_sensor, gain=GAIN)
            VRL = value * (5.0 / 32767.0)  # Convert to voltage (ADS1115 is 16-bit)
            
            # Calculate ammonia concentration in PPM
            ppm = get_ppm(VRL)

            # Print values to console
            print('Ammonia concentration:', round(ppm, 2), 'PPM')
            print('Voltage:', round(VRL, 2), 'V')
            print('-' * 20)
            time.sleep(1)

    except KeyboardInterrupt:
        print('Program stopped')

if __name__ == "__main__":
    main()
