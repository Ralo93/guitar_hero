import pyaudio
import numpy as np

def capture_audio():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = 1  # Duration of recording

    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format, channels=channels,
                    rate=fs, frames_per_buffer=chunk, input=True)

    frames = []

    # Capture audio data
    for _ in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(np.frombuffer(data, dtype=np.int16))

    stream.stop_stream()
    stream.close()
    p.terminate()

    return np.hstack(frames)
