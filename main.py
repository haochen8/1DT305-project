import sys
sys.path.append('lib')

import lib.dht as dht
import machine
import time
import urequests
import lib.wifiConnection as wifiConnection
import lib.datacake_keys as datacake_keys

# DHT11 Sensor
tempSensor = dht.DHT11(machine.Pin(27)) # DHT11 Constructor 

# WiFi Connection
ip = wifiConnection.connect()
print("Device IP:", ip)

# Check Internet Connection
try:
    response = urequests.get("http://www.google.com")
    print("Internet connection verified")
    response.close()
except Exception as e:
    print("No internet connection:", e)

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
            'device': '644972db-76c1-402d-a784-83a6c456cd84', # Device Serial Number
            'temperature': temperature,
            'humidity': humidity
        }
        print("Payload:", payload) # Debugging
        try:
            response = urequests.post(datacake_keys.DATACAKE_API_URL, headers=headers, json=payload)
            print("Datacake response status:", response.status_code) 
            print("Datacake response text:", response.text)
            response.close()
        except Exception as e:
            print("Error while sending data:", e)
    except Exception as error:
        print("Exception occurred:", error)
    time.sleep(15)  # Send updates every 15 seconds