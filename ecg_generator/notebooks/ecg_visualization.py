import matplotlib.pyplot as plt
import config

def plot_ecg(time, signal, title="ECG Signal"):
    plt.figure(figsize=(config.size_x,config.size_y))
    plt.plot(time, signal, color='blue')
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()

def plot_peaks(time, signal, peak_times, peaks):
    plt.figure(figsize=(10,4))
    plt.plot(time, signal, label="ECG", color='blue')
    plt.scatter(peak_times, peaks, color="red", label="Detected Heartbeats")
    plt.title("Heartbeat Detection")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid()
    plt.show()