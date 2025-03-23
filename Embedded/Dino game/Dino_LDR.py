import time                                                                                                                                                                                                                                                                                                                                                      
import board
import analogio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

ldr = analogio.AnalogIn(board.A0)
keyboard = Keyboard(usb_hid.devices)

while True:
    ldr_value = ldr.value
    print(ldr_value)                                                                                                                                               
    if ldr_value >= 15200:
        keyboard.press(Keycode.SPACEBAR)
        time.sleep(0.1)
        keyboard.release(Keycode.SPACEBAR)
    else:
        time.sleep(0.1)
