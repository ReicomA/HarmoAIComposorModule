import glob
import pickle
import numpy
import pandas as pd
from music21 import converter, instrument, note, chord
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import BatchNormalization as BatchNorm
from tensorflow.keras.utils import to_categorical 
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import load_model

from music21 import converter, instrument, note, chord, duration, stream, meter

import parse

TARGET_CHORD_MODEL = "Ludwig van Beethoven-4-chord.h5"
TARGET_CHORD_TABLE = "data/chord_map"

TARGET_DURATION_MODEL = "Ludwig van Beethoven-4-duration.h5"
TARGET_DURATION_TABLE = "data/duration_map"

MAX_NOTE = 20

def load_generator_table(target_root, result_type):
    table = {}
    file_stream = open(target_root, "r")

    lines = file_stream.readlines()
    file_stream.close()
    for line in lines:
        parsed_str = parse.parse("{}:{}", line)
        if result_type == "chord":
            table[int(parsed_str[1])] = parsed_str[0]
        elif result_type == "duration":
            table[int(parsed_str[1])] = float(parsed_str[0])

    return table

def load_table(target_root, result_type):
    table = {}
    file_stream = open(target_root, "r")

    lines = file_stream.readlines()
    file_stream.close()
    for line in lines:
        parsed_str = parse.parse("{}:{}", line)
        if result_type == "chord":
            table[parsed_str[0]] = int(parsed_str[1])
        elif result_type == "duration":
            table[float(parsed_str[0])] = int(parsed_str[1])

    return table


# 노트 불러오기
def load_notes(target_root):
    notes = None
    with open(target_root, 'rb') as filepath:
        notes = pickle.load(filepath)
    return notes

# 길이 불러오기
def load_durations(target_root):
    durations = None
    with open(target_root, 'rb') as filepath:
        durations = pickle.load(filepath)
    return durations

# 시퀸스 생성
def prepare_chord_sequences(notes, table, n_vocab):
    """ Prepare the sequences used by the Neural Network """
    sequence_length = 100
    network_input = []
    output = []
    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([table[char] for char in sequence_in])
        output.append(table[sequence_out])

    n_patterns = len(network_input)

    # reshape the input into a format compatible with LSTM layers
    normalized_input = numpy.reshape(network_input, (n_patterns, sequence_length, 1))
    # normalize input
    normalized_input = normalized_input / float(n_vocab)

    return (network_input, normalized_input)

def prepare_duration_sequences(durations, table, n_vocab):
    """ Prepare the sequences used by the Neural Network """
    sequence_length = 100
    network_input = []
    output = []
    for i in range(0, len(durations) - sequence_length, 1):
        sequence_in = durations[i:i + sequence_length]
        sequence_out = durations[i + sequence_length]
        network_input.append([table[char] for char in sequence_in])
        output.append(table[sequence_out])

    n_patterns = len(network_input)

    # reshape the input into a format compatible with LSTM layers
    normalized_input = numpy.reshape(network_input, (n_patterns, sequence_length, 1))
    # normalize input
    normalized_input = normalized_input / float(n_vocab)

    return (network_input, normalized_input)


def generate(model, network_input, generate_table, n_vocab):
    
    start = numpy.random.randint(0, len(network_input)-1)
    pattern = network_input[start]
    prediction_output = []

    for note_index in range(MAX_NOTE):
        prediction_input = numpy.reshape(pattern, (1, len(pattern), 1))
        prediction_input = prediction_input / float(n_vocab)

        prediction = model.predict(prediction_input, verbose=0)

        index = numpy.argmax(prediction)
        result = generate_table[index]
        prediction_output.append(result)

        pattern.append(index)
        pattern = pattern[1:len(pattern)]

    return prediction_output

""" 이 부분부터는 Only Test용 """
def create_midi(chord_output, duration_output):
    offset = 0
    # result note
    output_notes = []
    for i in range(len(chord_output)):

        pattern = chord_output[i]
        n_duration = duration_output[i]

        # in Chord
        if ('.' in pattern) or pattern.isdigit():
            
            notes_in_chord = pattern.split('.')
            notes = []

            # parse note
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = instrument.Piano()
                notes.append(new_note)
            
            # make chord
            new_chord = chord.Chord(notes, quarterLength=n_duration)
            new_chord.offset = offset
            output_notes.append(new_chord)
        
        # set Rest
        elif pattern == "rest":
            rest_note = note.Rest(quarterLength=n_duration)
            output_notes.append(rest_note)
        else:
            new_note = note.Note(pattern, quarterLength=n_duration)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)
        
        offset += 0.5

    return output_notes

def make_midi_file(midi_data, file_name, timeSignature):
    midi_stream = stream.Stream()
    midi_stream.append(meter.TimeSignature(timeSignature))
    midi_stream.append(midi_data)
    midi_stream.write('midi', file_name)
    midi_stream.show('text')


if __name__ == "__main__":
    #  모델 불러오기
    chord_model = load_model(TARGET_CHORD_MODEL)
    duration_model = load_model(TARGET_DURATION_MODEL)

    # 노트 데이터 불러오기
    notes = load_notes('data/notes')
    durations = load_durations('data/durations')

    # 해시 테이블 불러오기
    chord_table = load_table(TARGET_CHORD_TABLE, "chord")
    chord_n_vocab = len(chord_table.keys())

    duration_table = load_table(TARGET_DURATION_TABLE, "duration")
    duration_n_vocab = len(duration_table.keys())

    # 시퀸스 생성하기
    chord_network_input, chord_normalized_input = prepare_chord_sequences(notes, chord_table, chord_n_vocab)
    duration_network_input, duration_normalized_input = prepare_duration_sequences(durations, duration_table, duration_n_vocab)
    
    # Generate용 테이블 생성하기
    chord_table = load_generator_table(TARGET_CHORD_TABLE, "chord")
    duration_table = load_generator_table(TARGET_DURATION_TABLE, "duration")


    chord_output = generate(chord_model, chord_network_input, chord_table, chord_n_vocab)
    duration_output = generate(duration_model, duration_network_input, duration_table, duration_n_vocab)


    midi = create_midi(chord_output, duration_output)
    make_midi_file(midi, "test.mid", "4/4")