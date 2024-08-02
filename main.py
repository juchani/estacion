from machine import Pin
from time import sleep 
relay=Pin(21,Pin.OUT)
while True:
    relay.on()
    sleep(1)
    relay.off()
    sleep(1)