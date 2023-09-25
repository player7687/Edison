
import audioop
import matplotlib.pyplot as plt
import librosa.display
import numpy as np
import torch
import sys
import os
import soundfile as sf

from tempfile import NamedTemporaryFile

import io
from urllib.request import urlopen
# import pydub

from collections import Counter
from sklearn.preprocessing import LabelEncoder
from librosa.core import load
from librosa.feature import melspectrogram
from librosa import power_to_db
from .model import genreNet
from .config import GENRES

import warnings
warnings.filterwarnings("ignore")


def get_genre(file = None, input_link = None):
    le = LabelEncoder().fit(GENRES)
    # ------------------------------- #
    ## LOAD TRAINED GENRENET MODEL
    net         = genreNet()
    current_path = os.path.dirname(__file__)
    model_path = os.path.join(current_path, 'net.pt')
    net.load_state_dict(torch.load(model_path, map_location='cpu'))
    # ------------------------------- #
    ## LOAD AUDIO
    if file:
        audio_path  = file.file.name
        print(audio_path)
        y, sr       = load(audio_path, mono=True, sr=22050)
        data, sr = librosa.load(audio_path, sr=22050)
    else:
        # wav = io.BytesIO()

        # with urlopen(input_link) as r:
        #     r.seek = lambda *args: None  # allow pydub to call seek(0)
        #     pydub.AudioSegment.from_file(r).export(wav, "wav")

        # print(type(urlopen(input_link).read()))
        # print(dir(urlopen(input_link).read()))
        # print(type(io.BytesIO(urlopen(input_link).read())))
        # print(dir(io.BytesIO(urlopen(input_link).read())))

        # # print(wav.read())
        # wav.seek(0)
        # print(type(wav.read()))
        # # print(type(wav))
        # # print(dir(wav))
        # # print(type(wav.read()))
        # # print(wav.read())
        # # print(dir(wav.read()))
        # # print(type(urlopen(input_link)))
        # # print(dir(urlopen(input_link)))

        temp_file = NamedTemporaryFile(delete=False)
        temp_file.write(urlopen(input_link).read())
        audio_path = temp_file.name
        print(dir(temp_file))
        print(audio_path)

        y, sr       = load(audio_path, mono=True, sr=22050)
        data, sr = librosa.load(audio_path, sr=22050)
        temp_file.close()
        os.unlink(temp_file.name)
        print(temp_file)
        print(temp_file.name)
    # ------------------------------- #
    ## Plot of amplitude vs time (NEW!!!!)
    # data, sr = librosa.load(audio_path, sr=22050)
    # plt.figure(figsize=(14, 5))
    # librosa.display.waveshow(data, sr=sr) 
    # plt.show()
    # ------------------------------- #   
    ## Plot Spectograms
    X = librosa.stft(data)
    Xdb = librosa.amplitude_to_db(abs(X))
    # plt.figure(figsize=(14, 5))
    # librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz') 
    # plt.colorbar()
    # plt.show()
    # ------------------------------- # 
    ## Display MFCCs (Mel-Frequency Cepstral Coefficients)
    mfccs = librosa.feature.mfcc(data, sr=sr)
    # librosa.display.specshow(mfccs, sr=sr, x_axis='time')
    # plt.show()
    # ------------------------------- # 
    ## Zero Crossing Rat
    zeros = librosa.zero_crossings(data)
    # print("Zero Crossing rate: " ,sum(zeros))  
    # ------------------------------- # 
    ## GET CHUNKS OF AUDIO SPECTROGRAMS
    S           = melspectrogram(y, sr).T
    S           = S[:-1 * (S.shape[0] % 128)]
    num_chunk   = S.shape[0] / 128
    data_chunks = np.split(S, num_chunk)
    # ------------------------------- #
    ## CLASSIFY SPECTROGRAMS
    genres = list()
    for i, data in enumerate(data_chunks):
        data    = torch.FloatTensor(data).view(1, 1, 128, 128)
        preds   = net(data)
        pred_val, pred_index    = preds.max(1)
        pred_index              = pred_index.data.numpy()
        pred_val                = np.exp(pred_val.data.numpy()[0])
        pred_genre              = le.inverse_transform(pred_index).item()
        if pred_val >= 0.5:
            genres.append(pred_genre)
    # ------------------------------- #
    s           = float(sum([v for k,v in dict(Counter(genres)).items()]))
    pos_genre   = sorted([(k, v/s*100 ) for k,v in dict(Counter(genres)).items()], key=lambda x:x[1], reverse=True)
    # for genre, pos in pos_genre:
    #     print("%10s: \t%.2f\t%%" % (genre, pos))
    return pos_genre