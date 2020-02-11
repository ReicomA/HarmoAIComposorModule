import os
import glob
from music21 import converter, instrument, note, chord

from fractions import Fraction

import numpy as np
from tensorflow.keras.utils import to_categorical

# Maxlen은 테스트용
def get_data_list_for_ai(name, maxlen=None, timeSignature=2):
    # return 3 list, and 4 list

    # return list
    third_midi_path_list = []
    non_third_midi_path_list = []

    target_path = ""
    if name == "Chopin":
        target_path = "./data/chopin/*"
    elif name == "Beethoven":
        target_path = "./data/beethoven/*"
    elif name == "Scarlatti":
        target_path = "./data/scarlatti/*"
    else:
        raise ValueError("invalid name")

    # Make To Music
    path_list = glob.glob(target_path)
    

    # Return To Music21 Library
    midi_list = []
    for i in range(len(path_list)):
        midi_list.append(converter.parse(path_list[i]))
        if i == maxlen:
            break
    
    data_list = []

    for i in range(len(midi_list)):
        if midi_list[i].getTimeSignatures()[0].numerator%timeSignature == 0:
            data_list.append(midi_list[i])
    return data_list


def prepare_data(d_set):
    """ input data """

    """ return to.... """
    """
        data_list = {
            "chord" : []
            "duration" : []
        }
    """
    data_list = {"chord" : [], "duration" : []}

    
    for item in d_set:
        nots_to_parse = None
        try:
            parts = instrument.partitionByInstrument(item)
        except TypeError:
            print("## Some File occur error")
        
        if parts:
            print("## Some File Has Instrument parts")
            notes_to_parse = parts.parts[0].recurse()
        else:
            print("File has notes in a flat structure")
            notes_to_parse = item.flat.notes
        
        for element in notes_to_parse:
            if isinstance(element, note.Note):
                data_list["chord"].append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                data_list["chord"].append('.'.join(str(n) for n in element.normalOrder))
            elif isinstance(element, note.Rest):
                data_list["chord"].append("rest")

            # 길이
            if isinstance(element, note.Note) or isinstance(element, chord.Chord) or isinstance(element, note.Rest):
                if isinstance(element.duration.quarterLength, Fraction) == False:
                    if (element.duration.quarterLength <= 4 and element.duration.quarterLength > 0):
                        data_list["duration"].append(element.duration.quarterLength)
    
    return data_list

def make_mapping_table(note_arr):
    
    # 계이름 저장
    pitch_names = sorted(set(item for item in note_arr))

    # 계이름을 숫자로 전환
    note_to_int = dict((note, number) for number,  note in enumerate(pitch_names))
    return note_to_int

def make_n_vocab(datas):
    return len(set(datas))

# make sequence
def make_sequence(datas, mapping_table):

    sequence_len = 100
    n_vocab = make_n_vocab(datas)

    network_input = []
    network_output = []

    for i in range(0, len(datas) - sequence_len, 1):
        sequence_in = datas[i:i + sequence_len]
        sequence_out = datas[i + sequence_len]
        network_input.append([mapping_table[char] for char in sequence_in])
        network_output.append(mapping_table[sequence_out])

    n_patterns = len(network_input)

    # reshape the input into a format compatible witgh LSTM layers
    network_input = np.reshape(network_input, (n_patterns, sequence_len, 1))
    
    # 입력값 정규화
    network_input = network_input / float(n_vocab)
    network_output = to_categorical(network_output)

    return (network_input, network_output)
    
