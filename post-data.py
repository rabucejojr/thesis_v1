import requests

# Sensor values
temp = '33.2' #get data from rpi and dht11
humid = '2.0' #get data from rpi and dht11
nh3 = '20' #get data from rpi and mq137

# POST dht data: temperature and humidity
response = requests.post("https://dummyjson.com/posts/5")
response_dict = response.json()
print(response_dict)