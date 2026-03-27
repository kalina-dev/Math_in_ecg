import numpy as np

def detect_r_peaks(signal, time, threshold=0.8):
    """
    Detect R-peaks in ECG signal
    """
    peaks = []
    peak_times = []
    for i in range(1, len(signal)-1):
        if signal[i] > threshold and signal[i] > signal[i-1] and signal[i] > signal[i+1]:
            peaks.append(signal[i])
            peak_times.append(time[i])
    return np.array(peak_times), np.array(peaks)

def compute_heart_rate(peak_times):
    """
    Compute heart rate in BPM from detected peaks
    """
    intervals = np.diff(peak_times)
    if len(intervals) == 0:
        return 0
    avg_interval = np.mean(intervals)
    return 60 / avg_interval

def compute_rr_intervals(peak_times):
    """
    Compute RR intervals (time between consecutive R-peaks)
    """
    return np.diff(peak_times)

def hrv_statistics(rr_intervals):
    """
    Compute simple HRV metrics: mean and std of RR intervals
    """
    return np.mean(rr_intervals), np.std(rr_intervals)
    