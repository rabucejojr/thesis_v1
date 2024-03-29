import requests
import Adafruit_DHT
from time import sleep
import Adafruit_ADS1x15
from gpiozero import OutputDevice, AngularServo
import math

# MQ137 Configuration
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

# MQ Sensor Constants
RL = 47  # The value of resistor RL is 47K
m = -0.263  # Enter calculated Slope
b = 0.42  # Enter calculated intercept
Ro = 496.0725684427985  # Enter found Ro value
MQ_sensor = 0  # Sensor is connected to A0 on ADS1115

# DHT11 Pin Configuration
sensor = Adafruit_DHT.DHT11
pin = 27

# Relay Pin Configurations
pin1 = 17
pin2 = 22
relay1 = OutputDevice(pin1,active_high=False, initial_value=False)
relay2 = OutputDevice(pin2,active_high=False, initial_value=False)# change for configuration, solenoid2

# Servo Pin Configurations
servo = AngularServo(17,min_angle=-180,max_angle=180)

# API URL FOR BACKEND POST
api_temp = "https://piggery-backend.vercel.app/api/temperature"
api_humidity = "https://piggery-backend.vercel.app/api/humidity"
api_nh3 = "https://piggery-backend.vercel.app/api/ammonia"


def dht11():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    temperature = temperature * (9 / 5) + 32
    # Convert values to float
    temperature = float(temperature)
    humidity = float(humidity)
    return temperature, humidity


def mq137(VRL):
    Rs = ((5.0 * RL) / VRL) - RL  # Calculate Rs value
    ratio = Rs / Ro  # Calculate ratio Rs/Ro
    ppm = pow(10, ((math.log10(ratio) - b) / m))  # Calculate ppm
    return ppm


def solenoidValve(delay):  # execute relays to activate soleniod valves
    relay1.on()
    relay2.on()
    sleep(delay)
    relay1.off()
    relay2.off()
    sleep(delay)
    
def foodValveServo(delay):
    servo.angle = -180
    sleep(delay)
    servo.angle = 180
    sleep(delay)

def post_data(api, data, label):
    json_data = {"value": data}
    response = requests.post(api, json=json_data)
    if response.status_code == 201:
        print(label, "data sent successfully")
    else:
        print("Failed to send data to API:", response.text)


# Main Loop Execution
def main():
    while True:
        temperature, humidity = dht11()
        value = adc.read_adc(MQ_sensor, gain=GAIN)  # MQ137 adc reading
        VRL = value * (5.0 / 32767.0)
        ammonia = mq137(VRL)
        if temperature >= 35 or humidity >= 2.5:
            foodValveServo(30)
            solenoidValve(20)
        elif temperature is not None and humidity is not None:
            print("Temperature:", temperature)
            print("Humidity:", humidity)
            print("Ammonia:", round(ammonia, 2))
            # Post sensor readin to api
            post_data(api_temp, temperature, "Temperature")
            post_data(api_humidity, humidity, "Humidity")
            post_data(api_nh3, ammonia, "Ammonia")
            print("-" * 20)
            sleep(300)  # Reread after 5 minutes
            # check sensor readings are above threshold
            # if true, execute open relay/solenoid
            # to open pump to clean the area
            # and if done, open autofeeder to release feeds
            # if false, reread sensor readings until previous conditions are met


if __name__ == "__main__":
    main()
