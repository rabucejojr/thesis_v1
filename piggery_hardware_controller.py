import requests
import Adafruit_DHT
import time
import Adafruit_ADS1x15
import RPi.GPIO as GPIO
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
    return temperature, humidity


def get_ppm(VRL):
    Rs = ((5.0 * RL) / VRL) - RL  # Calculate Rs value
    ratio = Rs / Ro  # Calculate ratio Rs/Ro
    ppm = pow(10, ((math.log10(ratio) - b) / m))  # Calculate ppm
    return ppm


def mq137(VRL):
    Rs = ((5.0 * RL) / VRL) - RL  # Calculate Rs value
    ratio = Rs / Ro  # Calculate ratio Rs/Ro
    ppm = pow(10, ((math.log10(ratio) - b) / m))  # Calculate ppm
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
        ammonia = mq137()
        if temperature is not None and humidity is not None:
            print("Temperature:", temperature)
            print("Humidity:", humidity)
            print("Ammonia:", round(ammonia, 2))
            # Post sensor readin to api
            post_data(api_temp, temperature, "Temperature")
            post_data(api_humidity, humidity, "Humidity")
            post_data(api_nh3, ammonia, "Ammonia")
            print("-" * 20)
            time.sleep(300)  # Reread after 5 minutes
            # if temperature <= 32 and ammonia >= 25:
            #     relay(1, 1)
            #     time.sleep(5)
            #     # execute servo for autofeeder
            #     pwm.start(0)
            #     set_angle(90)
            #     pwm.stop()


if __name__ == "__main__":
    main()
