from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import text, sequence
from keras.utils.data_utils import get_file
from preprocess import preprocess
import pickle
import tensorflow as tf
import numpy as np
import pandas as pd

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

model = load_model('models/gru_cnn_custom.h5')
with open('models/tokenizer.pickle', 'rb') as f:
    tokenizer = pickle.load(f)

def predict(text, maxlen=150):
    text = ' '.join(preprocess(text))
    text = np.array([text])
    text = tokenizer.texts_to_sequences(text)
    text = sequence.pad_sequences(text, maxlen=maxlen)

    pred = model.predict(text)
    pred = pd.DataFrame(pred, columns=["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"])

    # Use some threshold to decide on what to return for has_bullying

    return pred

if __name__ == '__main__':
    print(predict('Haha, you are such an idiot!'))
