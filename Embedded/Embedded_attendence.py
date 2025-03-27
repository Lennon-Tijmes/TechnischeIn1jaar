from machine import Pin, SPI, PWM, I2C
import utime
from mfrc522 import MFRC522
import ds1302  # DS1302 RTC Library
from i2c_lcd import I2cLcd
import time
import socket
import network
import _thread

# Wi-Fi
SSID = "Red Milk"
PASSWORD = "01234567"

# DS1302 RTC (CLOCK, DATA, RS)
rtc = ds1302.DS1302(Pin(16), Pin(17), Pin(18))

# LCD
i2c = I2C(1, sda=Pin(10), scl=Pin(11), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

# people: {uid: (name, inside)}
registered = {
    584189687505: {"name": "Lennon", "inside": False}
}

# HTML global
html = ""

# The RGB LED
LED_BLUE = Pin(13, Pin.OUT)
LED_RED = Pin(14, Pin.OUT)
LED_GREEN = Pin(15, Pin.OUT)

# Buzzers
BUZZER1 = Pin(19, Pin.OUT)
BUZZER2 = Pin(20, Pin.OUT)

buzzer1_pwm = PWM(BUZZER1)
buzzer2_pwm = PWM(BUZZER2)

# Log for the webserver
access_logs = []

#=================Webserver==========#
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        utime.sleep(1)
    print(f"Connected to Wi-Fi: {wlan.ifconfig()[0]}")
    return wlan

#================LED=============#
def set_led(red, green, blue):
     LED_RED.value(red)
     LED_GREEN.value(green)
     LED_BLUE.value(blue)
    
#============RFID=============#
def init_rfid():
    return MFRC522(sck=2, mosi=3, miso=4, rst=0, cs=1)


def read_rfid(rfid):
    rfid.init()
    (status, tag_type) = rfid.request(rfid.REQIDL)
    if status == rfid.OK:
        (status, uid) = rfid.anticoll()
        if status == rfid.OK:
            return int.from_bytes(bytes(uid), "little")  
    return None

#===============BUZZERS===================#
def play_buzzer(buzzer, frequency, duration):
    buzzer.freq(frequency)
    buzzer.duty_u16(32768)
    utime.sleep(duration)
    buzzer.duty_u16(0)


def play_sound(frequencies, durations):
     for i, freq in enumerate(frequencies):
        # Alternate between buzzer 1 and buzzer 2
        if i % 2 == 0:
            play_buzzer(buzzer1_pwm, freq, durations[i])  # Play on buzzer 1
        else:
            play_buzzer(buzzer2_pwm, freq, durations[i])  # Play on buzzer 2    


def play_rejection():
    rejection_frequencies = [300, 250, 200, 150, 100, 150, 200, 250, 300]
    durations = [0.2] * len(rejection_frequencies)
    play_sound(rejection_frequencies, durations)
    

def play_welcome():
    welcome_frequencies = [330, 370, 415, 466, 523, 554, 622, 659, 698]
    durations = [0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.5]  # Duration for each note
    play_sound(welcome_frequencies, durations)


def play_goodbye():
    # Zelda chest closing sound (reverse melody)
    goodbye_frequencies = [698, 659, 622, 554, 523, 466, 415, 370, 330]
    durations = [0.5, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2]  # Reverse duration for each note
    play_sound(goodbye_frequencies, durations)

# ===== LCD TIME DISPLAY ===== #
def tag_time():
    Y, M, D, weekday, hr, m, s = rtc.date_time()
    return f"{D:02d}/{M:02d}/{Y} {hr:02d}:{m:02d}:{s:02d}"


def display_time():
    current_time = time.localtime()
    day, month, year = current_time[2], current_time[1], current_time[0]
    hour, minute, second = current_time[3], current_time[4], current_time[5]
    
    lcd.clear()
    lcd.move_to(3, 0)
    lcd.putstr(f"{day:02d}/{month:02d}/{year}")
    lcd.move_to(4, 1)
    lcd.putstr(f"{hour:02d}:{minute:02d}:{second:02d}")

#=======Logs and access========#
def check_acss(uid):
    date, time_str = display_time()
    
    if uid in registered:
        user = registered[uid]
        
        if not user["inside"]:
            status = "Inside"
            lcd.clear()
            print(f"Welcome {user['name']}")
            user["inside"] = True
            set_led(0, 1, 0)
            lcd.putstr(f"Welcome {user['name']}")
            play_welcome()
        else:
            status = "Outside"
            lcd.clear()
            print(f"Goodbye {user['name']}")
            user["inside"] = False
            set_led(1, 0, 1)
            lcd.putstr(f"Goodbye {user['name']}")
            play_goodbye()
    else:
        status = "Unauthorized"
        lcd.clear()
        print(f"No entry: {uid}")
        set_led(1, 0, 0)
        lcd.putstr("Unauthorized\n")
        lcd.putstr(str(uid))
        play_rejection()

    access_logs.insert(0, (date, time_str, user['name'] if uid in registered else "Unknown", status))
    utime.sleep(2)

def check_access(uid):
    current_time = tag_time()

    if uid in registered:
        user = registered[uid]
        if "events" not in user:
            user["events"] = []  # Ensure the user has an 'events' list
        
        last_status = user["events"][-1]["status"] if user["events"] else None
        new_status = "Checked Out" if last_status == "Checked In" else "Checked In"

        user["events"].append({"time": current_time, "status": new_status})

        if new_status == "Checked In":
            set_led(0, 1, 0)
            lcd.clear()
            lcd.putstr(f"Welcome {user['name']}")
            play_welcome()
        else:
            set_led(1, 0, 1)
            lcd.clear()
            lcd.putstr(f"Goodbye {user['name']}")
            play_goodbye()

    else:
        set_led(1, 0, 0)
        lcd.clear()
        lcd.putstr("Unauthorized")
        lcd.move_to(0, 1)
        lcd.putstr(str(uid))
        play_rejection()



def update_html():
    table_rows = "".join(
        f"<tr><td>{event['time']}</td><td>{registered[uid]['name']}</td><td>{event['status']}</td></tr>"
        for uid in registered for event in registered[uid].get("events", [])
    )
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Attendance Log</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 10px; border: 1px solid black; }}
            th {{ background: #ddd; }}
        </style>
    </head>
    <body>
        <h1>Attendance Log</h1>
        <table>
            <thead>
                <tr><th>Time</th><th>Name</th><th>Status</th></tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </body>
    </html>
    """
    return html  # Add return statement


def start_webserver():
    ip = network.WLAN(network.STA_IF).ifconfig()[0]
    addr = socket.getaddrinfo(ip, 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Prevents "Address already in use" error
    s.bind(addr)
    s.listen(5)

    print(f"Web server running at {ip}:80")

    while True:
        try:
            conn, addr = s.accept()
            request = conn.recv(1024).decode("utf-8")
            print(f"Received request from {addr}")  # Debugging

            response = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + update_html()
            conn.sendall(response.encode())  # Ensure the response is sent completely
        except Exception as e:
            print(f"Error handling request: {e}")  # Print any errors
        finally:
            conn.close()  # Always close the connection


def main():
    connect_wifi()
    print("Updating HTML page...")
    update_html()  # Generate the initial HTML page
    rfid = init_rfid()
    print("Waiting for RFID card...")

    while True:
        display_time()
        set_led(0, 0, 1)
        start_webserver()
        uid = read_rfid(rfid)
        if uid is not None:
            print(f"Scanned Card UID: {uid}")
            check_access(uid)
        utime.sleep(1)

        
        
if __name__ == "__main__":
    main()
