from flask import Flask, jsonify, request
import Adafruit_DHT
import board
import RPi.GPIO as GPIO
import mysql.connector
from datetime import datetime
import json
import time
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# SENSORS SETUP/PINOUT
# Setup GPIO pin for DHT11 sensor
sensor = Adafruit_DHT.DHT11
pin = 27

# MySQL Configuration
db_config = {
    "host": "localhost",
    "user": "admin",
    "password": "admin",
    "database": "sensors",
}


# Save DHT11 Temperature and Humidity
def save_dht_reading(temperature, humidity):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dht_temp (temp) VALUES (%s)", (temperature,))
        conn.commit()
        cursor.execute("INSERT INTO dht_humid (humid) VALUES (%s)", (humidity,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Error inserting data:", e)
        return False


# Start DHT11 Humidity and Temperature reading
@app.route("/insert-dht-data")
def insert_data():
    while True:
        try:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            temperature = temperature * (9 / 5) + 32
            if temperature is not None and humidity is not None:
                save_dht_reading(temperature, humidity)
                return jsonify({"temperature": temperature, "humidity": humidity})
            else:
                return jsonify({"error": "Failed to retrieve data from sensor"}), 500
        except RuntimeError as error:
            return jsonify({"error": str(error)}), 500
        except Exception as error:
            return jsonify({"Error": str(error)}), 500


# Fetch DHT11 temperature and humidity
@app.route("/dht11-temp", methods=["GET"])
def get_dht_temp():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dht_temp")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        # Convert fetched data to JSON format
        data = []
        for row in rows:
            created_at = datetime.strftime(
                row[2], "%Y-%m-%d %H:%M:%S"
            )  # Format date as dd/mm/yyyy HH:MM:SS

            data.append({"id": row[0], "value": row[1], "created_at": created_at})
        # Return JSON response
        return jsonify(data), 200
    except Exception as e:
        print("Error inserting data:", e)
        return False
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/dht11-humid", methods=["GET"])
def get_dht_humid():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dht_humid")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        # Convert fetched data to JSON format
        data = []
        for row in rows:
            created_at = datetime.strftime(
                row[2], "%Y-%m-%d %H:%M:%S"
            )  # Format date as dd/mm/yyyy HH:MM:SS
            data.append({"id": row[0], "humid": row[1], "created_at": created_at})
        # Return JSON response
        return jsonify(data), 200
    except Exception as e:
        print("Error inserting data:", e)
        return False
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Start MQ137 reading
@app.route("/mq137")  # ,,methods=['POST']
def get_mq137_reading():
    try:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        temperature = temperature * (9 / 5) + 32
        if temperature is not None and humidity is not None:
            save_data(temperature, humidity)
            return jsonify({"temperature": temperature, "humidity": humidity})
        else:
            return jsonify({"error": "Failed to retrieve data from sensor"}), 500
    except RuntimeError as error:
        return jsonify({"error": str(error)}), 500
    except Exception as error:
        return jsonify({"error": str(error)}), 500


# End MQ137 reading


@app.route("/test")
def hello_world():
    return "test"


if __name__ == "__main__":
    app.run(host="192.168.0.105", port=5000)
