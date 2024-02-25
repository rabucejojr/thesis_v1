from flask import Flask, jsonify, request
import Adafruit_DHT
import board
import RPi.GPIO as GPIO
import mysql.connector
from datetime import datetime
import json

app = Flask(__name__)

# SENSORS SETUP/PINOUT
# Setup GPIO pin for DHT11 sensor
sensor = Adafruit_DHT.DHT11
pin = 27

# MySQL Configuration
db_config={
    'host':'localhost',
    'user':'admin',
    'password':'admin',
    'database':'sensors',
    }

def save_data(temperature,humidity):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dht11 (temp, humid) VALUES (%s, %s)", (temperature, humidity))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Error inserting data:", e)
        return False

# Start DHT11 Humidity and Temperature reading
@app.route('/temp') # ,,methods=['POST']
def get_dht_reading():
    while True:
        try:
            humidity,temperature = Adafruit_DHT.read_retry(sensor, pin)
            #Get DHT11 Temperature and Humidity Data
#             temperature = sensor.temperature
#             #Convert temperature to Celcuis
            temperature = temperature *(9/5) + 32
#             humidity = sensor.humidity
            if humidity is not None and temperature is not None:
    #             print(f'Temperature={temperature:.2f}°C, Humidity={humidity:.2f}%')
                save_data(temperature,humidity)
                return jsonify({"Temperature":temperature,"Humidity":humidity})

            else:
                return jsonify ({"Runtime Error":str(error)}),500
#             print('Failed to retrieve data from sensor')
#             return jsonify({"Temperature":temperature,"Humidity":humidity})
        except RuntimeError as error:
             return jsonify ({"Runtime Error":str(error)}),500
        except Exception as error:
             return jsonify({"Error":str(error)}),500
# End DHT11 Temperature and Humidity reading

@app.route('/test')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run(host='192.168.254.192', port=5000)