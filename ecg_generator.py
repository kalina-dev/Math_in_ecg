import numpy as np
import json
import config

def ecg_beat(t):
    """
    Single ECG heartbeat as sum of Gaussian waves
    """
    data={}
    with open("ecg_config.json", "r") as file:
        data=json.load(file)

    #print(data)
    cfg = data.get("P", {"a": 0.01, "b": 0.01, "c": 0.01})
    P = gaussian(t, cfg.get("a"), cfg.get("b"), cfg.get("c"))
    cfg = data.get("Q", {"a": 0.01, "b": 0.01, "c": 0.01})
    Q = gaussian(t, cfg.get("a"), cfg.get("b"), cfg.get("c"))
    cfg = data.get("R", {"a": 0.01, "b": 0.01, "c": 0.01})
    R = gaussian(t, cfg.get("a"), cfg.get("b"), cfg.get("c"))
    cfg = data.get("S", {"a": 0.01, "b": 0.01, "c": 0.01})
    S = gaussian(t, cfg.get("a"), cfg.get("b"), cfg.get("c"))
    cfg = data.get("T", {"a": 0.01, "b": 0.01, "c": 0.01})
    T = gaussian(t, cfg.get("a"), cfg.get("b"), cfg.get("c"))
    return P + Q + R + S + T
    
def generate_normal_ecg(beats=config.beats, samples=config.samples):
    """
    Generate normal ECG with regular heartbeat intervals
    """
    t = np.linspace(0, 1, samples)
    beat = ecg_beat(t)
    signal = np.tile(beat, beats)
    time = np.linspace(0, beats, len(signal))
    return time, signal

def generate_arrhythmia_ecg(beats=config.beats, samples=config.samples):
    """
    Generate arrhythmic ECG with irregular intervals
    """
    signal = []
    time = []
    offset = 0
    for i in range(beats):
        stretch = np.random.uniform(0.7, 1.3)
        t = np.linspace(0, stretch, samples)
        beat = ecg_beat(t/stretch)
        signal.extend(beat)
        time.extend(t + offset)
        offset += stretch
    return np.array(time), np.array(signal)

def gaussian(t, mu, sigma, amplitude):
    """
    Gaussian wave function for ECG components
    """
    return amplitude * np.exp(-((t - mu)**2) / (2 * sigma**2))

def generate_ecg(duration=5, heart_rate=70):

    t = np.linspace(0, duration, duration * config.fs)

    signal = np.zeros_like(t)

    beat_period = config.min_const / heart_rate

    for beat in np.arange(0, duration, beat_period):
        signal += ecg_beat(t - beat)

    return t, signal

