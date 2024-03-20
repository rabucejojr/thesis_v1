import requests

# GET request
getSample = "http://piggery-backend.vercel.app/api/ammonia"
response = requests.get(getSample)

print(response.json())

print("Start POST request")
# POST request
postSample = "http://piggery-backend.vercel.app/api/ammonia"
data = {"value": 100.25}
response = requests.post(postSample, json=data)

print(response.json())
print("End POST request")
