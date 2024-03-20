import Adafruit_DHT
import time

# Set the sensor type: DHT11, DHT22, or AM2302
SENSOR = Adafruit_DHT.DHT11

# Set the GPIO pin where the sensor is connected
PIN = 27


def read_dht_sensor():
    # Attempt to get a sensor reading
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    temperature = temperature * (9 / 5) + 32
    # Check if reading was successful
    if humidity is not None and temperature is not None:
        print(f"Temperature={temperature:.2f}°C, Humidity={humidity:.2f}%")
    else:
        print("Failed to retrieve data from sensor")


# Call the function to read the sensor data
while True:
    read_dht_sensor()
    time.sleep(1)
