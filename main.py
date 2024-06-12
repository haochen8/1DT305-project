import sys
sys.path.append('lib')

import lib.dht as dht
import machine
import time
import urequests
import lib.wifiConnection as wifiConnection
import lib.datacake_keys as datacake_keys

# Datacake API details
DATACAKE_API_URL = "https://api.datacake.co/integrations/api/0f4fbf64-d7b3-42c4-b5aa-9646d7c3d4a2/"
DATACAKE_TOKEN = ""

tempSensor = dht.DHT11(machine.Pin(27)) # DHT11 Constructor 

# WiFi Connection
ip = wifiConnection.connect()
print("Device IP:", ip)


while True:
    try:
        tempSensor.measure()
        temperature = tempSensor.temperature()
        humidity = tempSensor.humidity()
        print("Temperature is {} degrees Celsius and Humidity is {}%".format(temperature, humidity))

        # Send data to Datacake
        headers = {
            'Authorization': 'Token {}'.format(datacake_keys.DATACAKE_TOKEN),
            'Content-Type': 'application/json'
        }
        payload = {
            'temperature': temperature,
            'humidity': humidity
        }
        response = urequests.post(datacake_keys.DATACAKE_API_URL, headers=headers, json=payload)
        response.close()
    except Exception as error:
        print("Exception occurred", error)
    time.sleep(15)  # Send updates every 15 seconds