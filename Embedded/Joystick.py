import time
import board
import analogio 	# Read analog values
import digitalio	# Read digital (clickity button)
import usb_hid		# Makes it seen as USB
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# use adafruit library
mouse = Mouse(usb_hid.devices)
kbd = Keyboard(usb_hid.devices)

# Setup analog inputs for joystick
x_axis = analogio.AnalogIn(board.A0)  # GP26 (Right-Left)
y_axis = analogio.AnalogIn(board.A1)  # GP27 (Up-Down)

button = digitalio.DigitalInOut(board.GP22)
button.switch_to_input(pull=digitalio.Pull.UP) # low 0 if pressed

button1 = digitalio.DigitalInOut(board.GP6)
button1.switch_to_input(pull=digitalio.Pull.UP)

button2 = digitalio.DigitalInOut(board.GP7)
button2.switch_to_input(pull=digitalio.Pull.UP)

# Sensitivity settings
SPEED = 15  # SPEEED
DEADZONE = 1500  # Ignore small movements I hate stick drift

last_keys = set()

# It's 16 bits so 65535.
# and half of it is 32768 which is the center.
# 0 should be when it's full left or down, 65535 is full right or up
def read_joystick():
    raw_x = x_axis.value - 32768  # Center is ~32768
    raw_y = y_axis.value - 32768  # Center is ~32768
    button_pressed = not button.value  # Button is active LOW

    # deadzone to ignore tiny movements
    if abs(raw_x) < DEADZONE:
        raw_x = 0
    if abs(raw_y) < DEADZONE:
        raw_y = 0

 # for the x. up should go up... that's why I used the y.
 # for the y. left was positive (so it moved to the right) so thats why I made it negative
    move_x = int((raw_x / 32768) * SPEED)  # Swap X and Y
    move_y = int((-raw_y / 32768) * SPEED)  # Inverted it to make it work properly

    return move_x, move_y, button_pressed, raw_x, raw_y

while True:
    x, y, btn, raw_x, raw_y = read_joystick()

    keys_to_press = set()

    # Move the mouse
    mouse.move(x, y)

    # Handle button press as left click
    if btn:
        mouse.press(Mouse.LEFT_BUTTON)
    else:
        mouse.release(Mouse.LEFT_BUTTON)

    if raw_x < -DEADZONE:
        keys_to_press.add(Keycode.A)
    if raw_x > DEADZONE:
        keys_to_press.add(Keycode.D)
    if raw_y < -DEADZONE:
        keys_to_press.add(Keycode.S)
    if raw_y > DEADZONE:
        keys_to_press.add(Keycode.W)

    for key in keys_to_press:
        if key not in last_keys:  # Only press if not already pressed
            kbd.press(key)

    for key in last_keys:
        if key not in keys_to_press:
            kbd.release(key)

    last_keys = keys_to_press

    if not button1.value:
        kbd.press(Keycode.SHIFT)
    else:
        kbd.release(Keycode.SHIFT)
        
    if not button2.value:
        kbd.press(Keycode.P)
    else:
        kbd.release(Keycode.P)

    time.sleep(0.02)