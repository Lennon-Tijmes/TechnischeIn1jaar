from machine import Pin
import utime

LEDRED = Pin(1, Pin.OUT) #LED at GP1
LEDGREEN = Pin(2, Pin.OUT) # LED as well
Button = Pin(4, Pin.IN, Pin.PULL_UP)

while True:				#Do Forever
    if Button.value() == 0: # If button is pressed
        LEDRED.value(1) # Turns it on
    else:
        LEDRED.value(0) # Turn off
        
    LEDGREEN.value(1)
    utime.sleep(1)
    LEDGREEN.value(0)
    utime.sleep(1)