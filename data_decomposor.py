import os
import glob
from music21 import converter, instrument, note, chord

# Maxlen은 테스트용
def get_data_list_for_ai(name, maxlen=None):
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

    # 박자대로 분류
    data_list = { 2 : [],  3 : [] }

    for i in range(len(midi_list)):
        if midi_list[i].getTimeSignatures()[0].numerator%3 == 0:
            data_list[3].append(midi_list[i])
        elif midi_list[i].getTimeSignatures()[0].numerator%2 == 0:
            data_list[2].append(midi_list[i])

    return data_list


def prepare_data(d_set):
    """ input data """

    """ return to.... """
    """
        data_list = {
            2 : { "chord" : d_list, "duration" : d_list }
            3 : { "chord" : d_list, "duration" : d_list }
        }
    """
    data_list = {                               \
        2 : { "chord" : [], "duration" : [] },  \
        3 : { "chord" : [], "duration" : [] }   \
    }

    # 2,4박자
    