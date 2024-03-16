import requests
import Adafruit_DHT
import time
import Adafruit_ADS1x15

#MQ137 Configuration
adc = Adafruit_ADS1x15.ADS1115()

#MQ137 Constants
GAIN = 1
V_RL = 0.1  # Sensor output voltage in clean air
Sensitivity = 1.0  # Sensor sensitivity in PPM/V

#DHT11 Pin Configuration
sensor = Adafruit_DHT.DHT11
pin = 27

# Sensor values
temp = [] #get data from rpi and dht11
humid = [] #get data from rpi and dht11
nh3 = [] #get data from rpi and mq137

# API URL FOR BACKEND POST
api_url = "https://jsonplaceholder.typicode.com/posts"

def dht11():
   humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
   temperature = temperature *(9/5) + 32
   # Convert values to float
   temperature = float(temperature)
   humidity = float(humidity)
   temperature=temp
   humidity=humid
   
   temp_value = {
    "value": temp,
   }
   humid_value = {
      "value": humid,
   }
   
   # POST dht data: temperature
   temp_res = requests.post(api_url,json=temp_value)
   res = temp_res.json()
   print(res)
   # POST dht data: humidity
   humid_res = requests.post(api_url,json=humid_value)
   res = humid_res.json()
   print(res)

def mq137():
   value = adc.read_adc(0,gain=GAIN)
   value = value * (4.09 / 32767.0)
   ppm = (value - V_RL) / Sensitivity
   print(value)
   print("Ammonia concentration:", ppm, "PPM")
   value = float(value)
   value =nh3
   time.sleep(0.5)
   
   nh3_value = {
   "value": nh3,
   }
   # POST dht data: ammonia
   nh3_res = requests.post(api_url,json=nh3_value)
   res = nh3_res.json()
   print(res)


# Infinite Loop

   