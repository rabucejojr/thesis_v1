from flask import Flask, jsonify, request
import Adafruit_DHT
import board
import RPi.GPIO as GPIO
import mysql.connector
from datetime import datetime
import json

# API Initialization
app = Flask(__name__)

# RPi pin configurations for sensors
# For DHT11/22
dht = Adafruit_DHT.DHT11
pin = 27
# For MQ137 for Ammonia Reading


# MySQL Configuration
db_config = {
    "host": "localhost",
    "user": "admin",
    "password": "admin",
    "database": "sensors",
}


# SAVE DHT11/22 Reading/s
def save_dht_data(temperature, humidity):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO dht11 (temp, humid) VALUES (%s, %s)", (temperature, humidity)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Error inserting data:", e)
        return False


# SAVE DHT11/22 Reading/s
def save_mq_data(ammonia):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO mq137 (ammonia) VALUES (%s)", (ammonia))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Error inserting data:", e)
        return False


# Start DHT11 Humidity and Temperature reading
@app.route("/temp", methods=["POST"])  # ,
def get_dht_reading():
    while True:
        try:
            # Get DHT11 Temperature and Humidity Data
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            temperature = temperature * (9 / 5) + 32
            if humidity is not None and temperature is not None:
                # Save readings to MYSQL
                save_dht_data(temperature, humidity)
                return jsonify({"Temperature": temperature, "Humidity": humidity})
            else:
                return jsonify({"Runtime Error": str(error)}), 500
        except RuntimeError as error:
            return jsonify({"Runtime Error": str(error)}), 500
        except Exception as error:
            return jsonify({"Error": str(error)}), 500


# End DHT11 Temperature and Humidity reading

# @app.route('/mq137',methods=['POST'])
# def get_ammonia_reading():
#     while True:
#         try:

# Run Flask API
if __name__ == "__main__":
    app.run(host="192.168.254.192", port=5000)
