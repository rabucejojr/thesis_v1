import time
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1

# Define analog input pin
analog_in = adc.read_adc(0, gain=GAIN)


def read_analog_average(pin, num_samples=500):
    """Read analog pin and return average of num_samples"""
    sum_values = 0
    for _ in range(num_samples):
        sum_values += pin.value
    return sum_values / num_samples


def convert_to_voltage(reading):
    """Convert ADC reading to voltage"""
    return reading * 5.0 / 65535.0


def calculate_RS_air(voltage):
    """Calculate sensor resistance in fresh air"""
    return ((5.0 * 10.0) / voltage) - 10.0


def calculate_R0(RS_air):
    """Calculate R0"""
    return RS_air / 3.6


while True:
    # Read analog value and convert to voltage
    sensor_value = read_analog_average(analog_in)
    sensor_voltage = convert_to_voltage(sensor_value)

    # Calculate RS_air and R0
    RS_air = calculate_RS_air(sensor_voltage)
    R0 = calculate_R0(RS_air)

    # Print R0
    print("R0 =", R0)

    # Wait for 1 second
    time.sleep(1)
