import requests
import Adafruit_DHT
import datetime
now = datetime.datetime.now()

# GET request
getSample = "http://piggery-backend.vercel.app/api/ammonia"
response = requests.get(getSample)

print (now)
# print(response.json())

print("Start POST request")
# POST request
postSample = "http://piggery-backend.vercel.app/api/ammonia"
data = {"value": 123.234}
response = requests.post(postSample, json=data)

print(response.json())
print("End POST request")
