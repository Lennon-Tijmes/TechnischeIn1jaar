from machine import Pin, PWM
import time

# Define buzzer pins
BUZZER1 = Pin(19, Pin.OUT)
BUZZER2 = Pin(20, Pin.OUT)

# Initialize PWM for buzzer
buzzer1_pwm = PWM(BUZZER1)
buzzer2_pwm = PWM(BUZZER2)

# Function to convert MIDI note to frequency
def midi_to_freq(midi_note):
    A4 = 440.0
    return A4 * 2 ** ((midi_note - 69) / 12)

# Play a note on a buzzer
def play_note(buzzer_pwm, frequency, duration):
    buzzer_pwm.freq(int(frequency))  # Set frequency
    buzzer_pwm.duty_u16(32768)  # Set volume (50%)
    time.sleep(duration)  # Play for the given duration
    buzzer_pwm.duty_u16(0)  # Turn off the buzzer

# Fixed time delay for each note in seconds
TIME_DELAY = 0.05  # 50 milliseconds delay between notes

# Main loop to read notes and play them
def play_notes():
    with open('/notes.txt', 'r') as file:
        for index, line in enumerate(file):
            note, velocity, time_delay = map(int, line.split())
            
            # If time_delay is zero, set it to a reasonable default (0.05 seconds)
            if time_delay == 0:
                time_delay = TIME_DELAY  # Use the fixed delay for notes with 0 time delay
            
            # Convert MIDI note to frequency
            frequency = midi_to_freq(note)  # Convert MIDI note to frequency
            
            # Alternate between the two buzzers for a richer sound
            if index % 2 == 0:
                print(f"Playing note {note} at {frequency} Hz for {TIME_DELAY} seconds (Buzzer 1).")
                play_note(buzzer1_pwm, frequency, TIME_DELAY)  # Play on buzzer 1
            else:
                print(f"Playing note {note} at {frequency} Hz for {TIME_DELAY} seconds (Buzzer 2).")
                play_note(buzzer2_pwm, frequency, TIME_DELAY)  # Play on buzzer 2

            time.sleep(0.1)  # Small pause between notes to avoid overlap (optional)

# Call play_notes to start the process
play_notes()
