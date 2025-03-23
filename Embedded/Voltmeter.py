from machine import Pin, Timer, ADC
import utime

voltMeter = ADC(26)

# GPIO pin mappings
LED_Segments = [0, 1, 2, 3, 4, 5, 6]  # GP for 7-segment segments (A-G)
LED_Digits = [7, 8, 9, 10]  # GP for 7-segment digits (Digit 1-4)
DP_Pin = 11 # GP for the Decimal Pointer

# Lists to store Pin objects
L = [Pin(pin, Pin.OUT) for pin in LED_Segments]  # Segment pins
D = [Pin(pin, Pin.OUT) for pin in LED_Digits]  # Digit control pins
DP = Pin(DP_Pin, Pin.OUT) # Decimal pointer

# 7-Segment display
LED_Bits = {
    '0': (1, 1, 1, 1, 1, 1, 0),  # 0
    '1': (0, 1, 1, 0, 0, 0, 0),  # 1
    '2': (1, 1, 0, 1, 1, 0, 1),  # 2
    '3': (1, 1, 1, 1, 0, 0, 1),  # 3
    '4': (0, 1, 1, 0, 0, 1, 1),  # 4
    '5': (1, 0, 1, 1, 0, 1, 1),  # 5
    '6': (1, 0, 1, 1, 1, 1, 1),  # 6
    '7': (1, 1, 1, 0, 0, 0, 0),  # 7
    '8': (1, 1, 1, 1, 1, 1, 1),  # 8
    '9': (1, 1, 1, 1, 0, 1, 1),  # 9
    ' ': (0, 0, 0, 0, 0, 0, 0)   # Blank
}

voltage = 0.0000  # variable for voltage

# Function to update the 7-segment display
def Refresh(timer):
    global voltage
    display_value = "{:.3f}".format(voltage)  # Makes it read as X.XXX
    display_value = display_value.replace('.', '')

    for dig in range(4):  # Loop through all 4 digits
        for segment in range(7):
            L[segment].value(LED_Bits[display_value[dig]][segment])  # Set segment states
        if dig == 0:  # This way the first decimal pointer will always be on
            DP.value(1)
        else:
            DP.value(0)
            
        D[dig].value(1)  # Enable decimal pointy thingy
        utime.sleep(0.005)  # Small delay
        D[dig].value(0)  # Disable decimal pointy thingy

# Initialize timer for refreshing display
tim = Timer()
tim.init(freq=50, mode=Timer.PERIODIC, callback=Refresh)

# Get the voltage from a scource (between 0v and 9.999v)
while True:
    voltMeter_value = voltMeter.read_u16() # we read it as a 16-bit number
    voltage = round((3.3 / 65535) * voltMeter_value * 3, 3) # we used 3 x 10k resistance
    utime.sleep(0.2)
