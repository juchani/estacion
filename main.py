from machine import Pin
from time import sleep 
relay=Pin(21,Pin.OUT)
while True:
    relay.on()
    sleep(5)
    relay.off()
    sleep(5)