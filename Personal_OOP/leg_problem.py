import time
import random
import threading
import pickle
import numpy as np
import pygame

pygame.init()

class Leg_Problem:
    def __init__(self, sleep_time=30):
        self.sleep_time = sleep_time
        self.remaining_time = sleep_time
        self.start_time = time.time()
        self.sitting = True
        self.sit_start = None
        self.auto_shocker = False # If you don't want to stand up and are too lazy
        self.running = True
        self.standing = False
        self.stand_start = None
        # When adding the ai part these needs to be initialized
        self.total_sit_time = 0
        self.total_stand_time = 0
        self.total_shocks = 0
        self.event_log = [] # Timestamp action remaining_time
    
    def update_time(self):
        if self.sitting:
            sitting_time = time.time() - self.start_time
            self.remaining_time -= sitting_time
        self.start_time = time.time() # Reset

    
    def sit(self):
        self.helper_sit()
        self.update_time()
        if self.sit_start:
            sit_duration = time.time() - self.sit_start
            self.total_sit_time += sit_duration
        self.sitting = True
        self.start_time = time.time() # just makin sure it starts here
        self.sit_start = time.time()
        self.event_log.append((time.time(), "sit", self.remaining_time))
        print(f"You are sitting. Time till it falls asleep: {int(self.remaining_time)}seconds")


    def helper_sit(self):
        if self.standing and self.stand_start is not None:
            stood_time = time.time() - self.stand_start
            multiplier = random.uniform(1.1  , 4)
            gained_time = stood_time * multiplier
            self.total_stand_time += stood_time
            self.remaining_time = min(self.sleep_time, self.remaining_time + gained_time)
            print(f"You stood for {int(stood_time)}s. Gained {int(gained_time)}s back")
            self.event_log.append((time.time(), f"stand_end", self.remaining_time))
            self.standing = False
            self.stand_start = None # clearing it after a use

    def stand(self):
        self.helper_sit()
        self.update_time()
        self.sitting = False
        self.standing = True
        self.start_time = time.time()
        self.stand_start = time.time()
        self.event_log.append((time.time(), "stand_start", self.remaining_time))
        print(f"You are standing, timer is paused")


    def shock(self):
        shock_gained_time = random.randint(60, 120)
        self.remaining_time = min(self.sleep_time, self.remaining_time + shock_gained_time)
        self.total_shocks += 1
        self.start_time = time.time()
        self.event_log.append((time.time(), "shock", self.remaining_time))
        pygame.mixer.Sound("Shock.mp3").play() # Makes the shock sound
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

    def get_suggestion(self):
        try:
            with open("AI_model.pkl", "rb") as f:
                data = pickle.load(f)
                model = data["model"]
                label_messages = data["label_messages"]

                sit_time = time.time() - self.sit_start if self.sit_start else 0

                input_data = [
                    min(sit_time, 60), # Made my datasets to 60 sec for presentation
                    min(self.total_stand_time, 60),
                    min(self.total_shocks, 30)
                ]

                # now for the classes so I can see what kind of messages
                # I will get
                label = model.predict([input_data])[0]
                messages = label_messages.get(label, ["No clue"])

                suggestion = random.choice(messages)
                print(f"Predicted: {label} | suggestion: {suggestion}")
                return suggestion
        except Exception as e:
            print(f"[ERROR] Failed to create a suggestion: {e}")
            return "Could not generate a suggestiong"            

if __name__ == "__main__":
    leg = Leg_Problem()
    leg.start_status_thread()

    print("Good boy commands: 'sit', 'stand X', 'shock', 'auto_shock', 'help', 'exit'")

    while True:
        time.sleep(1)
        asleep = leg.check_status()

        # GAMBLING
        if leg.auto_shocker and random.random() < 0.5: # 10% to shock every second!
            leg.shock()

        if asleep:
            print("Nooooo it fell asleep! Try to use 'shock' or 'stand'!")

        command = input("> ").strip().lower()

        if command == "sit":
            leg.sit()
        elif command.startswith("stand"):
            try:
                # Just to keep it for good old memory
                apples = int(command.split()[1])
                leg.stand()
            except (IndexError, ValueError):
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