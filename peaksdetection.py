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
