import mido

midi_file = "Bad_apple.mid"
mid = mido.MidiFile(midi_file)

for i, track in enumerate(mid.tracks):
    print(f"Track {i}: {track.name}")
    for msg in track:
        if msg.type == "note_on":
            print(f"Note: {msg.note}, Velocity: {msg.velocity}, Time: {msg.time}")

