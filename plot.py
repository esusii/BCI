import numpy as np
import cupy as cp
import matplotlib.pyplot as plt
import pyaudio
from time import sleep
from scipy.signal import find_peaks

# Parameters
CHUNK = 1024
RATE = 44100
DURATION = 5  # Duration to record in seconds
MAX_FRAMES = int(DURATION * RATE / CHUNK)
N_FRAMES_PLOT = 100  # Number of frames to plot

# Initialize PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paFloat32, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Initialize the plot
plt.ion()
fig, ax = plt.subplots()

# Record and process audio in chunks
frames = []
for i in range(MAX_FRAMES):
    data = cp.asarray(np.frombuffer(stream.read(CHUNK), dtype=np.float32))

    frames.append(data)

    # Only process and plot the most recent frames
    if len(frames) > N_FRAMES_PLOT:
        frames.pop(0)
        
    signal = cp.concatenate(frames)

    # Plot a small subset of the signal directly
    if i == 0:
        ax.plot(cp.asnumpy(signal[:1000]))
        ax.set_xlabel('Sample')
        ax.set_ylabel('Amplitude')
        ax.set_title('Raw EMG Data')

    plt.pause(0.001)
    ax.clear()

    # Sleep to simulate a live feed
    sleep(CHUNK / RATE)
