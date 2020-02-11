import pickle

# load notes data and duration data
def load_data():

    notes = None
    durations = None

    with open('data/notes', 'rb') as filepath:
        notes = pickle.load(filepath)

    with open('data/durations', 'rb') as filepath:
        durations = pickle.load(filepath)

    return (notes, durations)
