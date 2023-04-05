import numpy as np
import cupy as cp
import matplotlib.pyplot as plt
import pyaudio
from time import sleep
from scipy.signal import find_peaks

def gpu_stft(x, fs, window, nperseg, noverlap):
    step = nperseg - noverlap
    n_frames = (len(x) - noverlap) // step
    result = cp.empty((nperseg // 2 + 1, n_frames), dtype=cp.complex64)
    for i in range(n_frames):
        frame = x[i * step:i * step + nperseg] * window
        result[:, i] = cp.fft.rfft(frame)
    f = cp.fft.rfftfreq(nperseg, 1 / fs)
    t = cp.arange(n_frames) * step / fs
    return f, t, result

# Parameters
CHUNK = 1024
RATE = 44100
WINDOW = cp.hanning(512)
NPERSEG = 512
OVERLAP = NPERSEG // 2
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
    f, t, Zxx = gpu_stft(signal, RATE, WINDOW, NPERSEG, OVERLAP)

    # Find peaks in the STFT magnitude
    threshold = 0.1  # Set the threshold for peak detection
    peaks, _ = find_peaks(cp.asnumpy(cp.abs(Zxx[:, -1])), height=threshold)

    # Count the number of peaks above the threshold
    num_peaks = len(peaks)

    # Plot the STFT with peaks highlighted
    ax.pcolormesh(cp.asnumpy(t[-N_FRAMES_PLOT:]), cp.asnumpy(f), cp.asnumpy(cp.abs(Zxx[:, -N_FRAMES_PLOT:])), shading='gouraud')
    ax.set_ylim(0, 5000)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Frequency [Hz]')

    # Highlight the peaks on the plot
    ax.plot(cp.asnumpy(t[-1]), cp.asnumpy(f[peaks]), 'r.', markersize=10)

    # Add the peak count to the plot title
    ax.set_title(f'Number of Peaks: {num_peaks}')

    plt.pause(0.001)
    ax.clear()

    # Sleep to simulate a live feed
    sleep(CHUNK / RATE)
