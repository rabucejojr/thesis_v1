import requests

# Sensor values
temp = '33.2'
humid = '2.0'
nh3 = '20'
# POST dht data: temperature and humidity
response = requests.get("https://dummyjson.com/posts/5")
response_dict = response.json()
print(response_dict)