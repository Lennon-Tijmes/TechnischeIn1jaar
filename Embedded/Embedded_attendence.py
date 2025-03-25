from machine import Pin, SPI
import utime
from mfrc522 import MFRC522

# people: {uid: (name, inside)}
registered = {
    584189687505: ("Lennon", False),
}


def init_rfid():
    return MFRC522(sck=2, mosi=3, miso=4, rst=0, cs=1)


def read_rfid(rfid):
    rfid.init()
    (status, tag_type) = rfid.request(rfid.REQIDL)
    if status == rfid.OK:
        (status, uid) = rfid.anticoll()
        if status == rfid.OK:
            uid_number = int.from_bytes(bytes(uid))  # Convert UID to a number
            return uid_number
    return None


def check_access(uid):
    if uid in registered:
        name, inside = registered[uid]
        
        if not inside:
            print(f"Welcome {name}")
            registered[uid] = (name, True)
        else:
            print(f"Goodbye {name}")
            registered[uid] = (name, False)
    else:
        print("No entry")


def main():
    rfid = init_rfid()
    print("Waiting for RFID card...")

    while True:
        uid = read_rfid(rfid)
        if uid is not None:
            print(f"Scanned Card UID: {uid}")
            check_access(uid)
        utime.sleep(1)


if __name__ == "__main__":
    main()
