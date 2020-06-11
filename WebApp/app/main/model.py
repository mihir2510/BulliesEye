from keras.preprocessing import text, sequence
# from tensorflow.keras.models import load_model
from .preprocess import preprocess
import pickle
import numpy as np
import pandas as pd
import requests, json

import os, time
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# model = load_model('models/v1.h5')
# import os
# print('---------',os.getcwd()) #/home/kaustubhdamania/CodingStuff/Hackathons/SIH2020/BulliesEye/Ourapp/app/main/models
with open('./app/main/models/tokenizer.pickle', 'rb') as f:
    tokenizer = pickle.load(f)

labels = {
    0: 'toxic',
    1: 'severe_toxic',
    2: 'obscene',
    3: 'threat',
    4: 'insult',
    5: 'identity_hate'
}

threshold = 0.4

def predict(text, maxlen=150):
    text = ' '.join(preprocess(text))
    # print(text)
    text = np.array([text])
    text = tokenizer.texts_to_sequences(text)
    text = sequence.pad_sequences(text, maxlen=maxlen)

    data = json.dumps({"signature_name": "serving_default",
                   "instances": text.tolist()})
    headers = {"content-type": "application/json"}
    print('Sending request...')
    tac = time.time()
    json_response = requests.post('http://13.127.65.157:3000/v1/models/cb:predict',
                                data=data, headers=headers)
    tic = time.time()
    pred = np.array(json.loads(json_response.text)["predictions"])
    # print(pred.tolist(), 'okay')
    preddf = pd.DataFrame(pred, columns=["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"])

    # pred = model.predict(text)
    pred_list = pred.tolist()[0]
    # print(pred_list)
    toxic = pred_list[0]
    severe_toxic = pred_list[1]
    obscene = pred_list[2]
    threat = pred_list[3]
    insult = pred_list[4]
    identity_hate = pred_list[5]

    # Use some threshold to decide on what to return for has_bullying
    targets = []
    values = [severe_toxic, obscene, threat, insult, identity_hate]
    # print(values)
    for value in values:
        if value > threshold:
            targets.append(labels.get(values.index(value) + 1))
    has_bullying = False

    if len(targets):
        has_bullying = True
    score = toxic
    print(targets)
    return  ''.join([str(int(i)) for i in np.array(values) > threshold]), has_bullying, score

if __name__ == '__main__':
    import sys
    print(predict(' '.join(sys.argv[2:])))
