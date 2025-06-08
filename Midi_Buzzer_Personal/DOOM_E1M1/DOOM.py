from machine import Pin, PWM
import time

# Define pins for two buzzers
BUZZER1 = Pin(19, Pin.OUT)
BUZZER2 = Pin(20, Pin.OUT)

# Create PWM instances for both buzzers
buzzer1_pwm = PWM(BUZZER1)
buzzer2_pwm = PWM(BUZZER2)

# Function to convert MIDI note to frequency
def midi_to_freq(note):
    return 440 * (2 ** ((note - 69) / 12))

# Function to play a note on a given buzzer
def play_note(buzzer_pwm, frequency, duration):
    if frequency > 0:  # Avoid invalid frequencies
        buzzer_pwm.freq(int(frequency))  # Set frequency
        buzzer_pwm.duty_u16(32768)  # 50% duty cycle
        time.sleep(duration)  # Play for the given duration
        buzzer_pwm.duty_u16(0)  # Turn off the buzzer

# Function to read and play notes line-by-line (memory-efficient)
def play_notes():
    with open("notes.txt", "r") as f:
        for i, line in enumerate(f):  # Read one line at a time (low memory usage)
            parts = line.strip().split()
            if len(parts) == 3:
                try:
                    note = int(parts[0])
                    velocity = int(parts[1])
                    time_delay = int(parts[2]) / 1000  # Convert from ms to seconds

                    # Assign a minimal duration if time is 0
                    if time_delay == 0:
                        time_delay = 0.02

                    frequency = midi_to_freq(note)  # Convert MIDI note to frequency
                    print(f"Playing note {note} at {frequency:.2f} Hz for {time_delay:.3f} seconds.")

                    # Alternate between the two buzzers
                    if i % 2 == 0:
                        play_note(buzzer1_pwm, frequency, time_delay)
                    else:
                        play_note(buzzer2_pwm, frequency, time_delay)

                    time.sleep(time_delay)  # Respect note timing
                except ValueError:
                    print(f"Skipping invalid line: {line.strip()}")

# Run the play_notes function
play_notes()
