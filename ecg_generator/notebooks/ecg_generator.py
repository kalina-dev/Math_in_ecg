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
    # --- P WAVE ---
    # Small positive bump representing atrial contraction
    cfg = data.get("P", {"a": 0.01, "b": 0.01, "c": 0.01})
    P = gaussian(t, cfg.get("a"), cfg.get("b"), cfg.get("c"))

    # --- Q WAVE ---
    # Small negative dip before the main spike
    # Represents initial ventricular depolarization
    cfg = data.get("Q", {"a": 0.01, "b": 0.01, "c": 0.01})
    Q = gaussian(t, cfg.get("a"), cfg.get("b"), cfg.get("c"))

    # --- R WAVE ---
    # Large sharp peak (most prominent part of ECG)
    # Represents full ventricular contraction
    cfg = data.get("R", {"a": 0.01, "b": 0.01, "c": 0.01})
    R = gaussian(t, cfg.get("a"), cfg.get("b"), cfg.get("c"))

    # --- S WAVE ---
    # Negative dip right after the R peak
    # Completes ventricular depolarization
    cfg = data.get("S", {"a": 0.01, "b": 0.01, "c": 0.01})
    S = gaussian(t, cfg.get("a"), cfg.get("b"), cfg.get("c"))

    # --- T WAVE ---
    # Broader positive bump
    # Represents ventricular recovery (repolarization)
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
    """A Gaussian distribution, also known as a normal      distribution, is a continuous probability distribution characterized by its bell-shaped curve. It is defined by two parameters:
    μ (mu): The mean or expected value of the distribution
    σ (sigma): The standard deviation, which measures the spread of the distribution"""
    return amplitude * np.exp(-((t - mu)**2) / (2 * sigma**2))

def generate_ecg(duration=5, heart_rate=70):

    t = np.linspace(0, duration, duration * config.fs)

    signal = np.zeros_like(t)

    beat_period = config.min_const / heart_rate

    for beat in np.arange(0, duration, beat_period):
        signal += ecg_beat(t - beat)

    return t, signal

