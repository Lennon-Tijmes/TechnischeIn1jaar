import network
import utime

def scan_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    utime.sleep(2)  # giving it some time

    wifis = wlan.scan()

    network_set = set() # Empty until filled

    for w in wifis:
        # w[1] = BSSID, w[2] Wi-Fi Channel, w[4] Sec type, w[5] Hidden Stuff
        ssid = w[0].decode()  # Convert SSID to string
        rssi = w[3]  # Get signal strength (RSSI)
    
        if ssid:  # Ensure SSID is not empty
            network_set.add((ssid, rssi))

    # cool python, using the set, we give it a sort with the key
    # get the tuple of the RSSI (data structure of multiple parts)
    # But the lowest number is actually the strongest so we reverse it
    network_list = sorted(network_set, key=lambda x: x[1], reverse=True)

    # printing everything now that it is ordened
    print("\nAvailable Networks: ")
    for ssid, rssi in network_list:
        print(f"{ssid} 		{rssi}dBm")

scan_wifi()
