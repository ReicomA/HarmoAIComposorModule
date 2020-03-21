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

from time import time

from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from tensorflow.compat.v1.keras.backend import set_session
import tensorflow.compat.v1 as tf
"""CONFIG
    COMPOSOR_NAME = "song", "chopin", "scarlatti", "beetoven"
    TIME_SIGNATURE = "4", "3/4", "8"
            "4" --> 2/4 and 4/4
            "3/4" --> 3/4
            "8" --> 3/8 and 6/8
    EPOCHS
    BATCH_SIZE
"""
COMPOSOR_LIST = ["Frédéric Chopin", "Domenico Scarlatti", "Ludwig van Beethoven"]

COMPOSOR_NAME = COMPOSOR_LIST[2]
TIME_SIGNATURE = "4"
EPOCHS = 200
BATCH_SIZE = 512

DIR_PATH = "./maestro-v2.0.0/"
CSV_NAME = "maestro-v2.0.0.csv"

# 데이터 추출
def get_notes():

    notes = []
    midi_list = []

    #CSV 파일을 활용해 데이터 추출
    cv = pd.read_csv(DIR_PATH + CSV_NAME)

    # 파일을 검출하면서 동시에 박자도 파악해야함.
    for i in range(1, len(cv)):
        midi_file = cv[i:i+1]
        if midi_file["canonical_composer"][i] == COMPOSOR_NAME:
            root = DIR_PATH + str(midi_file["midi_filename"][i])
            print("checking...")
            one_midi = converter.parse(root)

            print(one_midi.getTimeSignatures()[0].ratioString)

            # 박자표 검토
            if TIME_SIGNATURE == "4":
                if (one_midi.getTimeSignatures()[0].ratioString == "4/4") or \
                    (one_midi.getTimeSignatures()[0].ratioString == "2/4"):
                    midi_list.append(one_midi)
                    print("Root %s is detected." % (root))

            elif TIME_SIGNATURE == "3/4":
                if one_midi.getTimeSignatures()[0].ratioString == "3/4":
                    midi_list.append(one_midi)
                    print("Root %s is detected." % (root))

            elif TIME_SIGNATURE == "8":
                if (one_midi.getTimeSignatures()[0].ratioString == "3/8") or \
                    (one_midi.getTimeSignatures()[0].ratioString == "6/8"):
                    midi_list.append(one_midi)
                    print("Root %s is detected." % (root))        
    print("%d midi file detected!" % len(midi_list))
    print("Start Parsing...")

    i = 0
    for midi in midi_list:
        print("Parsing..")
        notes_to_parse = None
        try:
            s2 = instrument.partitionByInstrument(midi)
            notes_to_parse = s2.parts[0].recurse()
        except:
            notes_to_parse = midi.flat.notes

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))
            elif isinstance(element, note.Rest):
                notes.append("rest")
        if i == 70:
            break
        else:
            i = i + 1
    print("files : %d\n" % i)


    # Save notes
    with open('data/notes', 'wb') as filepath:
        pickle.dump(notes, filepath)
    return notes
    
# 스트링값을 정수값으로 변환하는 딕셔너리 생성 및 파일 생성
def make_table(notes):

    pitch_names = sorted(set(item for item in notes))

    # 계이름을 숫자로 전환
    note_to_int = dict((note, number) for number, note in enumerate(pitch_names))

    # 파일 생성
    chord_map_stream = open("data/chord_map", "w")
    
    for note, number in note_to_int.items():
        if number == len(note_to_int) - 1:  
            chord_map_stream.write("%s:%d" % (note, number))
        else:
            chord_map_stream.write("%s:%d\n" % (note, number))
    chord_map_stream.close()

    return note_to_int

# 스퀸스 준비
def prepare_sequences(notes, table, n_vocab):
    sequence_length = 100

    network_input = []
    network_output = []

    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([table[char] for char in sequence_in])
        network_output.append(table[sequence_out])
    n_patterns = len(network_input)

    # reshape the input into a format compatible with LSTM layers
    network_input = numpy.reshape(network_input, (n_patterns, sequence_length, 1))
    # normalize input
    network_input = network_input / float(n_vocab)

    network_output = to_categorical(network_output)

    return (network_input, network_output)
    
def create_network(network_input, n_vocab):
    """ create the structure of the neural network """
    model = Sequential()
    model.add(LSTM(
        512,
        input_shape=(network_input.shape[1], network_input.shape[2]),
        recurrent_dropout=0.3,
        return_sequences=True
    ))
    model.add(LSTM(512, return_sequences=True, recurrent_dropout=0.3,))
    model.add(LSTM(512, return_sequences=True, recurrent_dropout=0.3,))
    model.add(LSTM(512, return_sequences=True, recurrent_dropout=0.3,))
    model.add(LSTM(512))
    model.add(BatchNorm())
    model.add(Dropout(0.3))
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(BatchNorm())
    model.add(Dropout(0.3))
    model.add(Dense(n_vocab))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    return model

def train(model, network_input, network_output):
    """ train the neural network """
    filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
    checkpoint = ModelCheckpoint(
        filepath,
        monitor='loss',
        verbose=0,
        save_best_only=True,
        mode='min',
		period=50
    )
    callbacks_list = [checkpoint]
    model.fit(network_input, network_output, epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=callbacks_list, validation_split=0.2)

if __name__ == '__main__':
    notes = get_notes()
    n_vocab = len(set(notes))
    table = make_table(notes)
    network_input, network_output = prepare_sequences(notes, table, n_vocab)

    """
    gpu_config = ConfigProto()
    gpu_config.gpu_options.allow_growth = True
    gpu_config.gpu_options.per_process_gpu_memory_fraction = 0.1
    ss = tf.Session(config=gpu_config)
    set_session(ss)
    """
    del notes
    del table

    model = create_network(network_input, n_vocab)
    train(model, network_input, network_output)
    # 모델 저장
    model.save('%s-%s-chord.h5' % (COMPOSOR_NAME, TIME_SIGNATURE))
    # ss.close()
