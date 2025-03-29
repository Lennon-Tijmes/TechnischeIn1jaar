import time
import random
import threading

class Leg_Problem:
    def __init__(self, sleep_time=30):
        self.sleep_time = sleep_time
        self.remaining_time = sleep_time
        self.start_time = time.time()
        self.sitting = True
        self.auto_shocker = False # If you don't want to stand up and are too lazy
        self.running = True
    
    def update_time(self):
        if self.sitting:
            sitting_time = time.time() - self.start_time
            self.remaining_time -= sitting_time
        self.start_time = time.time() # Reset

    
    def sit(self):
        self.update_time()
        self.sitting = True
        print(f"You are sitting. Time till it falls asleep: {int(self.remaining_time)}seconds")


    def stand(self, seconds):
        self.update_time()
        gained_time = seconds * 5
        self.remaining_time = min(self.sleep_time, self.remaining_time + gained_time) 
        self.start_time = time.time()
        print(f"Stood for {seconds}s, gained {gained_time}s. Time left: {int(self.remaining_time)}seconds")


    def shock(self):
        shock_gained_time = random.randint(60, 120)
        self.remaining_time = min(self.sleep_time, self.remaining_time + shock_gained_time)
        self.start_time = time.time()
        print(f"A 'non-lethal' shock has been administered, gained {shock_gained_time}seconds")


    def toggle_auto_shock(self):
        self.auto_shocker = not self.auto_shocker
        print(f"Auto-shock is now {'ON' if self.auto_shocker else 'OFF'}.")

    
    def check_status(self):
        self.update_time()
        if self.remaining_time <= 0:
            print("Your leg fell asleep...")
            if self.auto_shocker:
                self.shock()
            else:
                return True
            
        else:
            print(f"Time left: {int(self.remaining_time)}seconds")
        return False
    

    def start_status_thread(self):
        def status_loop():
            while self.running:
                time.sleep(2) # when it updates
                self.check_status()

        thread = threading.Thread(target=status_loop, daemon=True)
        thread.start()


if __name__ == "__main__":
    leg = Leg_Problem()
    leg.start_status_thread()

    print("Good boy commands: 'sit', 'stand X', 'shock', 'auto_shock', 'help', 'exit'")

    while True:
        time.sleep(1)
        asleep = leg.check_status()

        # GAMBLING
        if leg.auto_shocker and random.random() < 0.1: # 10% to shock every second!
            leg.shock()

        if asleep:
            print("Nooooo it fell asleep! Try to use 'shock' or 'stand'!")

        command = input("> ").strip().lower()

        if command == "sit":
            leg.sit()
        elif command.startswith("stand"):
            try:
                sec = int(command.split()[1])
                leg.stand(sec)
            except (ValueError):
                print("Use: Stand X (X = seconds...)")
        elif command == "shock":
            leg.shock()
        elif command == "auto_shock":
            leg.toggle_auto_shock()
        elif command == "help":
            print("commands: 'sit', 'stand X', 'shock', 'auto_shock', 'exit'")
        elif command == "exit":
            print("Goodbye, may your leg not sleep again!")
            leg.running = False
            break