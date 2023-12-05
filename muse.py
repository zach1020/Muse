# muse.py
import random
from midiutil import MIDIFile # Used to create midi files
import pygame # For playing the midi

# A pentatonic scale is made by taking an major scale and eliminating the 4th and 7th notes
# So, we generate a pentatonic melody by generating a melody without using 4 or 7

melody = []
pentatonic_scale = [0, 2, 4, 7, 9] # Degrees of scale to choose from
melody_octaves = [5, 6, 7] # Octaves to choose from, per midiutil's schema
melody_durations = [1, 2, 3, 4] # Duration of notes


for x in range(8): # 30-note melody
    # melody = [[scale-degree, duration], etc.]
    scale_degree = random.choice(pentatonic_scale)
    duration = random.choice(melody_durations)
    octave = random.choice(melody_octaves)
    scale_degree = scale_degree - 8 + (12 * octave) # Convert scale_degree to an absolute position on the keyboard
    melody.append([scale_degree, duration])
print(melody)

# Make a random arrangement of pentatonic thirds for the underlying chords
chords = []
# pent scale is the same
chord_octaves = [4, 5] 
chord_durations = [1, 2, 4]

for x in range(22): # 16 chords
    # chords = [[scale degree += 11 * octave, a "third" += 11 * octave, duration], etc.]
    scale_degree = random.choice(pentatonic_scale)
    third = 0
    # Determine what the "third" will be
    if scale_degree == 0:
        third = 7
    elif scale_degree == 2:
        third = 9
    elif scale_degree == 4:
        third = 11
    elif scale_degree == 7:
        third = 3
    elif scale_degree == 9:
        third = 5
        
    octave = random.choice(chord_octaves)
    scale_degree = scale_degree - 8 + (12 * octave) # Convert scale_degree and third to absolute positions on the keyboard for midiutil
    third = third - 8 + (12 * octave)
    duration = random.choice(chord_durations)
    
    chords.append([scale_degree, third, duration])

print(chords)

# Get the total duration of the piece
total_duration = max(sum(melody[1]), sum(chords[2]))
print(total_duration)


# Create MIDI file
track = 0
channel = 0
time = 0  # In beats
melody_time = 0
chord_time = 0
# duration = 1  # In beats
tempo = 34  # In BPM
volume = 100  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(3)  # Three tracks, defaults to format 1 (tempo track is created
# automatically)
MyMIDI.addTempo(track, time, tempo)
MyMIDI.addTempo(track+1, time, tempo)
MyMIDI.addTempo(track+2, time, tempo)

for x in range(7): # For each note in melody/chords
    # Add note to melody
    MyMIDI.addNote(track, channel, melody[x][0], melody_time, melody[x][1], 50)

    # Incrememnt melody time and chord time
    melody_time += melody[x][1]

for x in range(22):
    # Add note to chords
    MyMIDI.addNote(track+1, channel, chords[x][0], chord_time, chords[x][2], 25)
    # Add second chords note
    MyMIDI.addNote(track+2, channel, chords[x][1], chord_time, chords[x][2], 25)

    chord_time += chords[x][2]

with open("soothing_melody.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)






# Play the music with pygame

def play_music(midi_filename):
    clock = pygame.time.Clock()
    pygame.mixer.music.load(midi_filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(30)

# Initialize mixer
freq = 44100
bitsize = -16
channels = 2
buffer = 1024
pygame.mixer.init(freq, bitsize, channels, buffer)

play_music("soothing_melody.mid")
