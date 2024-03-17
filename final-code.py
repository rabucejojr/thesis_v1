import requests
import Adafruit_DHT
import time
import Adafruit_ADS1x15
import RPi.GPIO as GPIO

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

#Relay Pin Configurations
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT) # change for configuration, solenoid1
GPIO.setup(19,GPIO.OUT) # change for configuration, solenoid2

# API URL FOR BACKEND POST
api_temp = "https://piggery-backend.vercel.app/api/temperature"
api_humidity = "https://piggery-backend.vercel.app/api/humidity"
api_nh3 = "https://piggery-backend.vercel.app/api/ammonia"


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

def relay(relay1,relay2):
   #status refers to 0 for close, 1 for open
   GPIO.output(18,relay1) # relay for solenoid1
   GPIO.output(19,relay2) # relay for solenoid2

def post_data(api,data):
   json_data = {'value':data}
   response = requests.post(api,json=json_data)
   if response.status_code==201:
      print('Data sent successfully')
   else:
      print('Failed to send data to API:', response.text)

# Main Loop Execution
def main():
   while True:
      temperature, humidity = dht11()
      ammonia = mq137()
      if temperature is not None and humidity is not None and ammonia is not None:
         print(temperature,humidity,ammonia)
         post_data(api_temp,temperature)
         post_data(api_humidity,humidity)
         post_data(api_nh3,ammonia)
         time.sleep(1)
         if temperature <= 32 and ammonia >= 25:
            relay(1,1)
            time.sleep(5)
            # execute servo for autofeeder
            # code here
      
if __name__ == "__main__":
   main() 

