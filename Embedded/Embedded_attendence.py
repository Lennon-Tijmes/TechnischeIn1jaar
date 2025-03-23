from machine import Pin, SPI
import utime
from mfrc522 import MFRC522

rfid = MFRC522(sck=2, mosi=3, miso=4, rst=0, cs=1)

print("Test: read tag")

while True:
    rfid.init()
    
    (status, tag_type) = rfid.request(rfid.REQIDL)
    
    if status == rfid.OK:
        print("RFID tag wooop")
        
        (status, uid) = rfid.anticoll()
        if status == rfid.OK:
            print("Card UID: ", uid)
            print("CAAARD\n")
            
    utime.sleep(1)