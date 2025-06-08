from machine import Pin, PWM
import uasyncio as asyncio

# Define pins for three buzzers
BUZZER1 = Pin(19, Pin.OUT)
BUZZER2 = Pin(20, Pin.OUT)
BUZZER3 = Pin(21, Pin.OUT)

# Create PWM instances for all three buzzers
buzzer1_pwm = PWM(BUZZER1)
buzzer2_pwm = PWM(BUZZER2)
buzzer3_pwm = PWM(BUZZER3)

# Function to convert MIDI note to frequency
def midi_to_freq(note):
    return 440 * (2 ** ((note - 69) / 12))

# Function to play a note on a given buzzer
async def play_note(buzzer_pwm, frequency, duration):
    if frequency > 0:  # Avoid invalid frequencies
        buzzer_pwm.freq(int(frequency))  # Set frequency
        buzzer_pwm.duty_u16(32768)  # 50% duty cycle
        await asyncio.sleep(duration)  # Play for the given duration
        buzzer_pwm.duty_u16(0)  # Turn off the buzzer

# Imperial March melody (only the main theme, played by 3 buzzers alternately)
imperial_march = [
    # Buzzer 1, Buzzer 2, Buzzer 3 (Main melody notes)
    40, 40, 40, 38, 40, 45, 47, 40, 40, 40, 38, 40, 45, 47, 40, 47, 47, 47, 40, 38, 40,
    40, 40, 40, 38, 40, 45, 47, 40, 40, 40, 38, 40, 45, 47, 40, 40, 40, 38, 40, 45, 47, 40
]

# Function to play the Imperial March in a loop with alternating buzzers
async def play_imperial_march():
    buzzer_pins = [buzzer1_pwm, buzzer2_pwm, buzzer3_pwm]
    i = 0  # Start with the first buzzer
    while True:  # Loop to repeat the Imperial March continuously
        note = imperial_march[i]
        buzzer_pwm = buzzer_pins[i % 3]  # Alternate between the three buzzers
        await play_note(buzzer_pwm, midi_to_freq(note), 600 / 1000)  # Play each note for 600ms
        i += 1  # Move to the next note in the melody

# Run the play_imperial_march function with uasyncio
async def main():
    await play_imperial_march()

# Run the asyncio event loop
asyncio.run(main())
