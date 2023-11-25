import librosa
import pyaudio
from matplotlib import pyplot as plt
from matplotlib import animation
import random
import numpy as np
from contextlib import contextmanager
import time


most_recent_mfcc = None
S = None

class Rolling_FR:
    # optm: use circular array
    def __init__(self, LEN=100):
        self.max_len = LEN
        self.arr = []
        self.last_time = time.time()

    # def calc_avg(self):
    #     if len(self.arr) == 0: return 0
    #     return sum(self.arr) / len(self.arr)

    # def add_sample(self, n):
    #     self.arr.append(n)
    #     if len(self.arr) > self.max_len: self.pop(0)

    def make_sample(self):
        delta = time.time() - self.last_time
        self.last_time = time.time()

        self.arr.append(delta)
        if len(self.arr) > self.max_len:
            self.arr.pop(0)

        return sum(self.arr) / len(self.arr)
rolling_fr = Rolling_FR()


#### mic manager via pyaudio
# based on https://stackoverflow.com/a/62429797
FORMAT = pyaudio.paFloat32
CHANNELS = 1
SAMPLERATE = 96000
CHUNK = 1024 * 2

def mic_callback(in_data, frame_count, time_info, flag):
    numpy_array = np.frombuffer(in_data, dtype=np.float32)
    print(numpy_array.shape, rolling_fr.make_sample())
    global most_recent_mfcc, S
    # S = librosa.feature.melspectrogram(y=numpy_array, sr=SAMPLERATE, n_mels=128, fmax=8000)
    # most_recent_mfcc = librosa.feature.mfcc(S=librosa.power_to_db(S))
    return None, pyaudio.paContinue

@contextmanager
def make_microphone(callback):

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLERATE,
                    input=True,
                    output=False,
                    stream_callback=callback,
                    frames_per_buffer=CHUNK)

    try:
        yield stream
    finally:
        stream.close()
        p.terminate()

#### vis loop
VIS_LEN = 100

xs = []
ys = []
fig, axs = plt.subplots(nrows=2, sharex=True)
# S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)

def anim_frame(frame):
    print('anim frame called')
    if most_recent_mfcc is None: return
    for x in axs: x.clear()

    # from https://librosa.org/doc/0.10.1/generated/librosa.feature.mfcc.html#librosa.feature.mfcc
    # img = librosa.display.specshow(librosa.power_to_db(S, ref=np.max),
    #                             x_axis='time', y_axis='mel', fmax=8000,
    #                             ax=axs[0])
    # fig.colorbar(img, ax=[axs[0]])
    # axs[0].set(title='Mel spectrogram')
    # axs[0].label_outer()
    img = librosa.display.specshow(most_recent_mfcc, x_axis='time', ax=axs[1])
    fig.colorbar(img, ax=[axs[1]])
    axs[1].set(title='MFCC')



    # new_point = random.random()

    # if len(xs) > VIS_LEN:
    #     xs.pop(0)
    #     ys.pop(0)

    # xs.append(frame)
    # ys.append(new_point)

    # ax.plot(xs, ys)

with make_microphone(mic_callback) as stream:
    pass
    while True:
        time.sleep(0.01)
    # ani = animation.FuncAnimation(fig, anim_frame, interval=10)
    # plt.show()