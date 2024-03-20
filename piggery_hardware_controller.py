import requests
import Adafruit_DHT
import time
import Adafruit_ADS1x15
import RPi.GPIO as GPIO

# Global Variables
global temp, humid, nh3

# MQ137 Configuration
adc = Adafruit_ADS1x15.ADS1115()

# MQ137 Constants
GAIN = 1
V_RL = 0.1  # Sensor output voltage in clean air
Sensitivity = 1.0  # Sensor sensitivity in PPM/V

# DHT11 Pin Configuration
sensor = Adafruit_DHT.DHT11
pin = 27

# Relay Pin Configurations
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)  # change for configuration, solenoid1
GPIO.setup(19, GPIO.OUT)  # change for configuration, solenoid2

# Servo Pin Configurations
GPIO.setmode(GPIO.BCM)
servo_pin = 17
GPIO.setup(servo_pin, GPIO.OUT)
# Create a PWM object at 50Hz (20ms period)
pwm = GPIO.PWM(servo_pin, 50)


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
#     temperature = temp
#     humidity = humid
    return temperature, humidity


def mq137():
    value = adc.read_adc(0, gain=GAIN)
    value = value * (4.09 / 32767.0)
    ppm = (value - V_RL) / Sensitivity
    ppm = nh3
    print("value:", value)
    print("ppm:", ppm)
    print("Ammonia concentration:", ppm, "PPM")
    value = round(float(ppm), 2)
    return ppm


def relay(relay1, relay2):  # execute relays to activate soleniod valves
    # status refers to 0 for close, 1 for open
    GPIO.output(18, relay1)  # relay for solenoid1
    GPIO.output(19, relay2)  # relay for solenoid2


def set_angle(angle):
    duty = angle / 18 + 2
    # open valve
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(3)
    # close valve
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)


def post_data(api, data, label):
    json_data = {"value": data}
    response = requests.post(api, json=json_data)
    if response.status_code == 201:
        print(label,"data sent successfully")
    else:
        print("Failed to send data to API:", response.text)


# Main Loop Execution
def main():
    while True:
        temperature, humidity = dht11()
#         ammonia = mq137()
        if temperature is not None and humidity is not None:
            print("Temperature:", temperature)
            print("Humidity:", humidity)
            post_data(api_temp, temperature, 'Temperature')
            post_data(api_humidity, humidity, 'Humidity')
            print('=====DONE=====')
#             post_data(api_nh3, ammonia, 'Ammonia')
            time.sleep(150)
#             if temperature <= 32 and ammonia >= 25:
#                 relay(1, 1)
#                 time.sleep(5)
#                 # execute servo for autofeeder
#                 pwm.start(0)
#                 set_angle(90)
#                 pwm.stop()


if __name__ == "__main__":
    main()