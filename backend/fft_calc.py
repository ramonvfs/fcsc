import numpy as np

FREQUENCY = 50  # Frequency in Hz
SAMPLES = 256  # Number of samples

def calculate_fft(signal):
    n = len(signal)

    if n < 2:
        return np.array([]), np.array([])
    
    signal_clean = signal - np.mean(signal)
    fft_result = np.fft.fft(signal_clean)
    fft_magnitudes = np.abs(fft_result) / n
    frequencies = np.fft.fftfreq(n, d=1/FREQUENCY)[:n // 2]
    fft_magnitudes = fft_magnitudes[:n // 2]

    return frequencies, fft_magnitudes