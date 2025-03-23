import network
import socket
from machine import Pin
import utime
import dht

SSID = "Red Milk"
PASSWORD = "01234567"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    utime.sleep(1)
    
ip_address = wlan.ifconfig()[0]
print("Connected to WiFi")

# Relay
RELAY = Pin(16, Pin.OUT)
RELAY.value(0)  # Starts off

# DHT22
dht_pin = Pin(15, Pin.IN, Pin.PULL_UP)
dht22 = dht.DHT22(dht_pin)

LED_INTERNAL = Pin("LED", Pin.OUT)

# Globals
last_temp_read_time = 0
temperature = "N/A"
humidity = "N/A"
relay_status = "OFF"

def read_inside_temp():
    global last_temp_read_time, temperature, humidity
    current_time = utime.time()

    if current_time - last_temp_read_time >= 3:  # Read every 3 seconds
        try:
            LED_INTERNAL.value(1)
            dht22.measure()
            temperature = "{:.1f}°C".format(dht22.temperature() - 4)
            humidity = "{:.1f}%".format(dht22.humidity())
            LED_INTERNAL.value(0)
        except Exception as e:
            print("DHT22 Error:", e)
            temperature = "N/A"
            humidity = "N/A"
            LED_INTERNAL.value(0)

        last_temp_read_time = current_time  # Reset timer
        
html = """<!DOCTYPE html>
<html>
<head>
    <title>Mhmmm pico</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background-color: #f4f4f4; }
        h1 { color: #333; }
        .status-circle {
            width: 50px; height: 50px; margin: 10px auto;
            border-radius: 50%; background-color: red;
            display: flex; align-items: center; justify-content: center;
            font-weight: bold; color: white;
            transition: background-color 0.5s ease-in-out, transform 0.3s ease-in-out;
        }
        .on-btn { background-color: green; color: white; }
        .off-btn { background-color: red; color: white; }
        button { 
            font-size: 18px; padding: 10px 20px; margin: 10px; 
            border: none; cursor: pointer; border-radius: 5px; 
            transition: 0.3s; 
        }
        button:hover { opacity: 0.8; }
    </style>
    <script>
        function updateData() { 
            fetch('/data')
                .then(response => response.json())
                .then(data => {
                    // Update temperature & humidity without needing LED check
                    document.getElementById('temperature').innerText = data.temp;
                    document.getElementById('humidity').innerText = data.hum;
                
                    // Update relay status
                    document.getElementById('relay-status').innerText = data.relay;
                    let circle = document.getElementById('status-circle');

                    if (data.relay === "ON") {
                        circle.style.backgroundColor = "green";
                        circle.style.transform = "scale(1.1)";  // Slight pulse effect
                    } else {
                        circle.style.backgroundColor = "red";
                        circle.style.transform = "scale(1)";
                    }
                });
        }

        setInterval(updateData, 1000);  // Check relay status every second
    </script>
</head>
<body>
    <h1>Relay and Temperature :)</h1>
    <h2>Temperature: <span id="temperature">Getting Cookies...</span></h2>
    <h2>Humidity: <span id="humidity">Getting Milk...</span></h2>

    <h2>Relay Status: <span id="relay-status">OFF</span></h2>
    <div id="status-circle" class="status-circle"> </div>

    <button class="on-btn" onclick="fetch('/on')">Turn ON</button>
    <button class="off-btn" onclick="fetch('/off')">Turn OFF</button>
</body>
</html>
"""

# Start the webserver
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(5)

print("It's alive http://" + ip_address)

while True:
    try:
        conn, addr = s.accept()
        request = conn.recv(1024).decode("utf-8")

        # The  GET methods
        if "GET /on" in request:
            RELAY.value(1)
            relay_status = "ON"
        elif "GET /off" in request:
            RELAY.value(0)
            relay_status = "OFF"
        elif "GET /data" in request:
            read_inside_temp()
            data = '{{"temp": "{}", "hum": "{}", "relay": "{}"}}'.format(temperature, humidity, relay_status)
            conn.send("HTTP/1.1 200 OK\nContent-Type: application/json\n\n" + data)
            conn.close()
            continue  # Skip sending HTML for /data requests


        # Get HTML
        response = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + html
        conn.send(response)
        conn.close()

    except Exception as e:
        print("Error:", e)
