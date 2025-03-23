from machine import Pin, I2C
import utime
import ds1302  # DS1302 RTC Library
from i2c_lcd import I2cLcd
import dht

LED_BLUE = Pin("LED", Pin.OUT)

# DS1302 RTC (GPIO Pins: RS, DATA, CLK)
rtc = ds1302.DS1302(Pin(16), Pin(17), Pin(18))

# LCD
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)
lcd.clear()

# Gives back the weekday
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# DHT22 Sensor
dht_pin = Pin(15, Pin.IN, Pin.PULL_UP)
dht22 = dht.DHT22(dht_pin)

# **ONLY SET THE TIME ONCE, THEN COMMENT OUT THIS LINE**
# rtc.date_time((2025, 2, 14, 4, 10, 10, 00))  # (Year, Month, Day, DayOfWeek, Hour, Min, Sec)

last_temp_read_time = utime.time()  # Get last temperature read time
goodTemp = "N/A"  # So it displays something in the beginning


def get_rtc_time():
    year, month, day, weekday, hour, minute, second = rtc.date_time()
    date_str = "{} {}/{}/{}".format(DAYS[weekday], day, month, year)
    time_str = "{:02}:{:02}:{:02}".format(hour, minute, second)
    return date_str, time_str


def read_inside_temp():
    global last_temp_read_time, goodTemp

    current_time = utime.time()
    if current_time - last_temp_read_time >= 3:  # Read every 3 seconds
        try:
            LED_BLUE.value(1)
            dht22.measure()  # Get measurement
            insideTemp = dht22.temperature()  # Get temperature
            LED_BLUE.value(0)
            if insideTemp is not None:
                goodTemp = "{:.1f}{}C".format(insideTemp - 4, "\xDF")  # Adjust temp and display degree sign
            else:
                goodTemp = "N/A"
        except Exception as e:
            print("Error", e)
            goodTemp = "N/A"
            LED_BLUE.value(0)

        last_temp_read_time = current_time  # Reset timer


def update_lcd():
    date_str, time_str = get_rtc_time()

    lcd.move_to(0, 0)
    lcd.putstr(date_str)  # Display date

    lcd.move_to(0, 1)
    lcd.putstr(time_str)  # Display time

    lcd.move_to(10, 1)
    lcd.putstr(goodTemp)  # Display temperature


# Main Loop
while True:
    read_inside_temp()
    update_lcd()  # Refresh LCD
    utime.sleep(0.3)
