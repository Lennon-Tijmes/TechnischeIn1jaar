import mido

def midi_to_notes(midi_file):
    mid = mido.MidiFile(midi_file)
    notes = []
    
    for track in mid.tracks:
        for msg in track:
            if msg.type == "note_on":
                notes.append({
                    'note': msg.note,
                    'velocity': msg.velocity,
                    'time': msg.time
                })
    return notes

# Save notes to a file
midi_file = 'Tim.mid'  # Your MIDI file
notes = midi_to_notes(midi_file)

with open('notes.txt', 'w') as f:
    for note in notes:
        f.write(f"{note['note']} {note['velocity']} {note['time']}\n")
