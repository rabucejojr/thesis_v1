import requests
import Adafruit_DHT
import time
import Adafruit_ADS1x15

#Global Variables
temp, humid, nh3 = None

#MQ137 Configuration
adc = Adafruit_ADS1x15.ADS1115()

#MQ137 Constants
GAIN = 1
V_RL = 0.1  # Sensor output voltage in clean air
Sensitivity = 1.0  # Sensor sensitivity in PPM/V

#DHT11 Pin Configuration
sensor = Adafruit_DHT.DHT11
pin = 27

# API URL FOR BACKEND POST
api_url = "https://jsonplaceholder.typicode.com/posts"

def dht11():
   humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
   temperature = temperature *(9/5) + 32
   # Convert values to float
   temperature = float(temperature)
   humidity = float(humidity)
   temperature = temp
   humidity = humid
   return temperature,humidity 

def mq137():
   value = adc.read_adc(0,gain=GAIN)
   value = value * (4.09 / 32767.0)
   ppm = (value - V_RL) / Sensitivity
   ppm = nh3
   print('value:',value)
   print('ppm:',ppm)
   print("Ammonia concentration:", ppm, "PPM")
   value = round(float(ppm),2)
   return ppm

def post_data(data):
   json_data = {'value':data}
   response = requests.post(api_url,json=json_data)
   if response.status_code==201:
      print('Data sent successfully')
   else:
      print('Failed to send data to API:', response.text)

# Main Loop Execution
def main():
   while True:
      temperature, humidity = dht11()
      if temperature is not None and humidity is not None:
         print(temperature,humidity)
         post_data(temperature)
         post_data(humidity)
      ammonia = mq137()
      if ammonia is not None:
         print(ammonia)
         post_data(ammonia)
      time.sleep(1)
      
if __name__ == "__main__":
   main() 

