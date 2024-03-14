import requests

# Sensor values
# temp = '33.2' #get data from rpi and dht11
# humid = '2.0' #get data from rpi and dht11
# nh3 = '20' #get data from rpi and mq137

new_data = {
    "userID": 1,
    "id": 1,
    "title": "Making a POST request",
    "body": "This is the data we created."
}

# temp_value = {
#     "value": temp,
# }
# humid_value = {
#     "value": humid,
# }
# nh3_value = {
#     "value": nh3,
# }

# POST dht data: temperature and humidity
api_url = "https://jsonplaceholder.typicode.com/posts"
response = requests.post(api_url,json=new_data)
response_dict = response.json()
print(response_dict)