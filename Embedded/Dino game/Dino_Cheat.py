import time
import board
import analogio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import supervisor
import displayio

# Initialize keyboard
kbd = Keyboard(usb_hid.devices)

# Import screen capture functions
try:
    import screen_capture
except ImportError:
    print("Error: screen_capture module not found.")
    supervisor.reload()

# Set up pixel detection position
CHECK_X = 600  # Look for obstacles ahead of the dino
DINO_Y = 330    # Dino's foot Y position
DUCK_Y = 280    # If an obstacle is above this, we duck

# Function to check if an obstacle is present
def detect_obstacle():
    # Capture a small area where obstacles appear
    pixels = screen_capture.get_pixel(CHECK_X, DINO_Y)

    # If pixel is dark (indicating a cactus)
    if pixels and pixels[0] < 100:  # Black/dark pixels
        return "JUMP"

    # Check for airborne obstacles (birds)
    pixels_upper = screen_capture.get_pixel(CHECK_X, DUCK_Y)
    if pixels_upper and pixels_upper[0] < 100:
        return "DUCK"

    return None

# Main loop to play the game
while True:
    action = detect_obstacle()

    if action == "JUMP":
        kbd.press(Keycode.SPACE)
        time.sleep(0.1)
        kbd.release(Keycode.SPACE)

    elif action == "DUCK":
        kbd.press(Keycode.DOWN_ARROW)
        time.sleep(0.5)  # Duck slightly longer
        kbd.release(Keycode.DOWN_ARROW)

    time.sleep(0.02)  # Short delay to check again
