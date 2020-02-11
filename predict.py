"""
MIT License

Copyright (c) 2019 Sigurður Skúli Sigurgeirsson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from data_loader import *
from data_decomposor import *
from model import *

import numpy as np
from music21 import converter, instrument, note, chord, duration, stream

DATA_SIZE = 100

def make_sequence(datas, data_labels, n_vocab):

    data_to_int = dict((datas, number) for number, datas in enumerate(data_labels))
    sequence_len = 100
    network_input = []
    output = []

    for i in range(0, len(datas) - sequence_len, 1):
        sequence_in = datas[i:i + sequence_len]
        sequence_out = datas[i + sequence_len]
        network_input.append([data_to_int[char] for char in sequence_in])
        output.append(data_to_int[sequence_out])

    n_patterns = len(network_input)

    normalized_input = np.reshape(network_input, (n_patterns, sequence_len, 1))
    normalized_input = normalized_input / float(n_vocab)

    return (network_input, normalized_input)

def get_datas(model, network_input, data_labels, n_vocab, midi_range):
    
    """ random sequence """
    # pick a random sequence from the input as a starting point for the prediction
    start = np.random.randint(0, len(network_input)-1)

    int_to_note = dict((number, note) for number, note in enumerate(data_labels))

    pattern = network_input[start]
    prediction_output = []

    # generate 500 notes
    for note_index in range(midi_range):
        prediction_input = np.reshape(pattern, (1, len(pattern), 1))
        prediction_input = prediction_input / float(n_vocab)

        prediction = model.predict(prediction_input, verbose=0)

        index = np.argmax(prediction)
        result = int_to_note[index]
        prediction_output.append(result)

        pattern.append(index)
        pattern = pattern[1:len(pattern)]

    return prediction_output

def make_midi_data(raw_note_list, raw_duration_list):
    
    offset = 0
    # result note
    output_notes = []
    for i in range(len(raw_note_list)):

        pattern = raw_note_list[i]
        n_duration = raw_duration_list[i]

        # in Chord
        if ('.' in pattern) or pattern_isdigit():
            
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


def make_midi_file(midi_data, file_name):    
    midi_stream = stream.Stream(midi_data)
    midi_stream.write('midi', file_name)


if __name__ == "__main__":

    # load
    notes, durations = load_data()

    # make label
    note_labels = sorted(set(item for item in notes))
    durations_lables = sorted(set(item for item in durations))

    # make vocab
    notes_vocab = make_n_vocab(notes)
    durations_vocab = make_n_vocab(durations)

    # make inputs
    notes_inputs = make_sequence(notes, note_labels, notes_vocab)
    durations_inputs = make_sequence(durations, durations_lables, durations_vocab)

    # make model
    note_model = make_LSTM_model(notes_inputs[1], notes_vocab, True, "chord_weight.hdf5")
    durations_model = make_LSTM_model(durations_inputs[1], durations_vocab, True, "duration_weight.hdf5")

    # generate data
    result_midi_raw = get_datas(note_model, notes_inputs[0], note_labels ,notes_vocab, 10)
    result_durations_raw = get_datas(durations_model ,durations_inputs[0], durations_lables, durations_vocab, 10)

    # make midi_data
    midi = make_midi_data(result_midi_raw, result_durations_raw)
    # write midi
    make_midi_file(midi, "test.mid")

    # midi_result = make_midi_data(result_midi_raw, result_durations_raw)



    