# Import libraries
from machine import Pin # import Pin definitions
import time # import timer library

# define GP16 as output pin
redLED = Pin(16, Pin.OUT)

# start loop
while True:    
    redLED.on() # turn on green LED
    time.sleep(0.3) # wait 0.3 seconds
    redLED.off() # turn off green LED
    time.sleep(0.8) # wait 0.8 second
