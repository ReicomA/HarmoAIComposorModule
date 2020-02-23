from data_decomposor import *
import pickle

from model import *
from tensorflow.keras.callbacks import ModelCheckpoint

import tensorflow as tf

from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from tensorflow.compat.v1.keras.backend import set_session


""" COINFIG """
COMPOSER_NAME = "Chopin"
MAX_SHEET = 10 #Infinite
TIME_SIGNATURE = 2
EPOCHS = 20
BATCH_SIZE = 64


""" data save path """
CHORD_SAVE_PATH = "data/notes"
DURATION_SAVE_PATH = "data/durations"

# parsing data
music21_data = get_data_list_for_ai(COMPOSER_NAME, MAX_SHEET, TIME_SIGNATURE)
data_set = prepare_data(music21_data)

# save data
with open(CHORD_SAVE_PATH, 'wb') as filepath:
    pickle.dump(data_set["chord"], filepath)

with open(DURATION_SAVE_PATH, 'wb') as filepath:
    pickle.dump(data_set["duration"], filepath)

# make data table (str -> int)
chord_table = make_mapping_table(data_set["chord"])
duration_table = make_mapping_table(data_set["duration"])

# make sequence (input, output)
chord_sequence = make_sequence(data_set["chord"], chord_table)
duration_sequence = make_sequence(data_set["duration"], duration_table)


# train model
# 1. chord

HDF_FILE_PATH = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
check_point = ModelCheckpoint(          \
    HDF_FILE_PATH,                      \
    monitor='loss',                     \
    verbose=0,                          \
    save_best_only=True,                \
    mode='min',                         \
    period=10                          \
)


gpu_config = ConfigProto()
gpu_config.gpu_options.allow_growth = True
ss = InteractiveSession(config=gpu_config)
set_session(ss)

callbacks_list = [check_point]

    # make model
chord_model = make_LSTM_model(chord_sequence[0], make_n_vocab(data_set["chord"]))
chord_model.fit(chord_sequence[0], chord_sequence[1], epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=callbacks_list, validation_split=0.2)


duration_model = make_LSTM_model(chord_sequence[0], make_n_vocab(data_set["duration"]))
duration_model.fit(duration_sequence[0], duration_sequence[1], epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=callbacks_list, validation_split=0.2)
ss.close()