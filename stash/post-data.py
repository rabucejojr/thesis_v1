import requests

# import Adafruit_DHT
# sensor = Adafruit_DHT.DHT11
# pin = 27
# humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
# temperature = temperature *(9/5) + 32
# Convert values to float
# temperature = float(temperature)
# humidity = float(humidity)

# Dummy Data
new_data = {
    "userID": 1,
    "id": 1,
    "title": "Making a POST request",
    "body": "This is the data we created.",
}
api_url = "https://jsonplaceholder.typicode.com/posts"
response = requests.post(api_url, json=new_data)
response_dict = response.json()
print(response_dict)


# Sensor values
# temp = temperature #get data from rpi and dht11
# humid = humidity #get data from rpi and dht11
# nh3 = '20' #get data from rpi and mq137

# temp_value = {
#     "value": temp,
# }
# humid_value = {
#     "value": humid,
# }
# nh3_value = {
#     "value": nh3,
# }

# api_url = "https://jsonplaceholder.typicode.com/posts"

# # POST dht data: temperature
# response = requests.post(api_url,json=temp_value)
# res = response.json()
# print(res)

# # POST dht data: humidity
# response = requests.post(api_url,json=humid_value)
# res = response.json()
# print(res)

# # POST dht data: ammonia
# response = requests.post(api_url,json=nh3_value)
# res = response.json()
# print(res)
