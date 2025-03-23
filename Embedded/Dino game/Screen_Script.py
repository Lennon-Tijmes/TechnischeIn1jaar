import mss
import serial
import time

with open("debug_log.txt", "a") as f:
    f.write("Obstacle detected! Jump!\n")

pico = serial.Serial('COM8', 9600)  # Change COM8 if needed
time.sleep(2)  # Wait for connection

DINO_X = 640
DINO_Y = 410
OBSTACLE_X = 720
DUCK_Y = 350  # Adjust for flying birds

sct = mss.mss()

def get_pixel_color(x, y):
    """Capture a pixel color at (x, y) using mss."""
    screenshot = sct.grab(sct.monitors[1])  # Full-screen capture
    pixel = screenshot.pixel(x, y)
    return pixel  # Returns (R, G, B)

while True:
    print("Checking...")  # To verify the script is running

    cactus_color = get_pixel_color(OBSTACLE_X, DINO_Y)
    bird_color = get_pixel_color(OBSTACLE_X, DUCK_Y)

    print(f"Cactus color: {cactus_color}, Bird color: {bird_color}")  # Debugging

    if sum(cactus_color) < 200:  # Cactus detected
        print("Jump!")  # Should print multiple times
        pico.write(b'JUMP\n')
        time.sleep(0.1)  # Small delay to prevent spam

    elif sum(bird_color) < 200:  # Bird detected
        print("Duck!")
        pico.write(b'DUCK\n')
        time.sleep(0.1)

    time.sleep(0.05)


