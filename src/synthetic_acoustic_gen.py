"""
AcuDiag Synthetic Acoustic Generator
Generates mathematically grounded physical acoustic waveforms for home appliances:
- Healthy Baselines (50Hz mains hum, motor rotor harmonics, smooth bearing friction)
- Bearing Outer Race Spall (Ball pass frequency impacts + high-frequency resonance)
- Drum Imbalance / Misalignment (Low-frequency sinusoidal amplitude modulation at drum RPM)
- Drain Pump Cavitation (Broadband stochastic high-entropy noise bursts)
- AC Compressor Valve Leak (Harmonic gas whistling around 2.4 kHz)
- Speaker Replay Spoofing (DAC quantization, speaker impulse response, lack of physical low rumble)
"""

import numpy as np
from scipy import signal
from typing import Tuple, Dict, Optional


class ApplianceAcousticSynthesizer:
    def __init__(self, sample_rate: int = 44100, seed: Optional[int] = 42):
        self.sample_rate = sample_rate
        self.seed = seed
        self.rng = np.random.default_rng(seed)

    def _get_time_array(self, duration_sec: float) -> np.ndarray:
        return np.linspace(0, duration_sec, int(self.sample_rate * duration_sec), endpoint=False)

    def generate_healthy_baseline(self, duration_sec: float = 3.0) -> np.ndarray:
        """
        Synthesizes a normal, factory-healthy front-load washing machine sound:
        - 50 Hz electrical hum with soft 100 Hz harmonic
        - 400 RPM drum rotation (6.67 Hz fundamental rotation frequency)
        - Rotor pole harmonics (12 poles -> 80 Hz)
        - Colored airflow/bearing friction noise with natural high-frequency roll-off (SNR ~ 35dB)
        """
        t = self._get_time_array(duration_sec)
        
        # 1. 50Hz mains electrical hum + soft harmonic
        mains_hum = 0.15 * np.sin(2 * np.pi * 50.0 * t) + 0.05 * np.sin(2 * np.pi * 100.0 * t)
        
        # 2. Drum rotation (400 RPM = 6.67 Hz) smooth acoustic envelope
        drum_freq = 400.0 / 60.0
        drum_rumble = 0.20 * np.sin(2 * np.pi * drum_freq * t)
        
        # 3. Motor rotor pole harmonics (12 poles -> 80 Hz)
        motor_harmonic = 0.08 * np.sin(2 * np.pi * (drum_freq * 12) * t)
        
        # 4. Soft background air friction noise (lowpass filtered to emulate physical enclosure roll-off)
        raw_noise = self.rng.normal(0, 1, len(t))
        nyquist = 0.5 * self.sample_rate
        sos_air = signal.butter(2, min(3000.0 / nyquist, 0.99), btype='lowpass', output='sos')
        air_noise = signal.sosfilt(sos_air, raw_noise) * 0.03
        
        sig = mains_hum + drum_rumble + motor_harmonic + air_noise
        return sig / (np.max(np.abs(sig)) + 1e-9)

    def generate_bearing_fault(self, duration_sec: float = 3.0, severity: float = 1.0) -> np.ndarray:
        """
        Synthesizes Outer Race Bearing Spall (Ball Pass Frequency Outer Race - BPFO):
        - Characteristic periodic shock pulses occurring every time balls pass over surface micro-spall
        - Excites natural structural resonance of the machine housing (centered at 1,450 Hz)
        """
        t = self._get_time_array(duration_sec)
        healthy = self.generate_healthy_baseline(duration_sec) * 0.4
        
        # BPFO = ~3.05 * shaft frequency (6.67 Hz * 3.05 = ~20.35 Hz impact rate)
        bpfo = 20.35
        impact_period = int(self.sample_rate / bpfo)
        
        # Train of decaying exponential impulse bursts
        impacts = np.zeros(len(t))
        damp_time = 0.015  # 15ms decay
        damp_samples = int(self.sample_rate * damp_time)
        decay = np.exp(-np.linspace(0, 5, damp_samples))
        
        # Resonance frequency around 1,450 Hz
        carrier = np.sin(2 * np.pi * 1450.0 * np.linspace(0, damp_time, damp_samples))
        single_burst = decay * carrier
        
        for idx in range(0, len(t) - damp_samples, impact_period):
            impacts[idx:idx + damp_samples] += single_burst * severity * 0.8
            
        sig = healthy + impacts
        return sig / (np.max(np.abs(sig)) + 1e-9)

    def generate_drum_imbalance(self, duration_sec: float = 3.0, severity: float = 1.0) -> np.ndarray:
        """
        Synthesizes Drum Misalignment / Uneven Load:
        - Heavy suspension damper contact thump impulses excited at 65 Hz & 110 Hz
        - Motor load pulsation at 100 Hz mains second harmonic
        - Distinctive low-frequency amplitude modulation (< 300 Hz)
        """
        t = self._get_time_array(duration_sec)
        healthy = self.generate_healthy_baseline(duration_sec) * 0.4
        
        drum_freq = 400.0 / 60.0  # 6.67 Hz
        period_samples = int(self.sample_rate / drum_freq)
        
        # Suspension impact pulses at 6.67 Hz rate
        thump_len = int(self.sample_rate * 0.05)  # 50ms impulse response
        t_thump = np.linspace(0, 0.05, thump_len, endpoint=False)
        thump_pulse = np.exp(-t_thump / 0.015) * (1.0 * np.sin(2 * np.pi * 65.0 * t_thump) + 0.8 * np.sin(2 * np.pi * 110.0 * t_thump))
        
        thumps = np.zeros(len(t))
        for idx in range(0, len(t) - thump_len, period_samples):
            thumps[idx:idx + thump_len] += thump_pulse
            
        envelope = 1.0 + 0.6 * severity * np.sin(2 * np.pi * drum_freq * t)
        motor_strain = 0.25 * severity * np.sin(2 * np.pi * 100.0 * t) * envelope
        
        sig = (healthy * envelope) + (thumps * 1.2 * severity) + motor_strain
        return sig / (np.max(np.abs(sig)) + 1e-9)

    def generate_pump_cavitation(self, duration_sec: float = 3.0, severity: float = 1.0) -> np.ndarray:
        """
        Synthesizes Drain Pump Cavitation / Air Lock:
        - Stochastic micro-bubble collapse creating sharp, high-entropy acoustic bursts
        - Bandlimited to pump volute acoustic cavity resonance (2.8 kHz - 5.5 kHz)
        - Modulated by impeller blade pass frequency (150 Hz)
        """
        t = self._get_time_array(duration_sec)
        healthy = self.generate_healthy_baseline(duration_sec) * 0.3
        
        nyquist = 0.5 * self.sample_rate
        low_cut = max(2800.0 / nyquist, 0.01)
        high_cut = min(5500.0 / nyquist, 0.99)
        sos_pump = signal.butter(4, [low_cut, high_cut], btype='bandpass', output='sos')
        
        raw_bursts = self.rng.normal(0, 1, len(t))
        filtered_bursts = signal.sosfilt(sos_pump, raw_bursts)
        
        # Modulated by 150 Hz blade pass frequency
        impeller_mod = 0.5 + 0.5 * np.sin(2 * np.pi * 150.0 * t)
        cavitation_bursts = filtered_bursts * impeller_mod * severity * 0.9
        
        sig = healthy + cavitation_bursts
        return sig / (np.max(np.abs(sig)) + 1e-9)

    def generate_compressor_valve_leak(self, duration_sec: float = 3.0, severity: float = 1.0) -> np.ndarray:
        """
        Synthesizes AC Compressor Valve Leak (Problem Space #9 Appliance Class):
        - High-pressure refrigerant gas whistling through valve reed orifice at ~2,400 Hz
        - Harmonic resonance at 4,800 Hz
        - Turbulent orifice hiss (2.0 kHz - 3.2 kHz)
        - Amplitude modulated by compressor piston stroke frequency (50 Hz)
        """
        t = self._get_time_array(duration_sec)
        healthy = self.generate_healthy_baseline(duration_sec) * 0.4
        
        # 2,400 Hz whistle + 4,800 Hz harmonic
        whistle = 0.6 * np.sin(2 * np.pi * 2400.0 * t) + 0.15 * np.sin(2 * np.pi * 4800.0 * t)
        
        # Turbulent gas hiss around 2.4 kHz
        nyquist = 0.5 * self.sample_rate
        low_cut = max(2000.0 / nyquist, 0.01)
        high_cut = min(3200.0 / nyquist, 0.99)
        sos_hiss = signal.butter(4, [low_cut, high_cut], btype='bandpass', output='sos')
        raw_hiss = signal.sosfilt(sos_hiss, self.rng.normal(0, 1, len(t))) * 0.35
        
        # Modulate by 50 Hz compressor cycle
        stroke_mod = 0.6 + 0.4 * np.sin(2 * np.pi * 50.0 * t)
        leak_component = (whistle + raw_hiss) * stroke_mod * severity * 0.85
        
        sig = healthy + leak_component
        return sig / (np.max(np.abs(sig)) + 1e-9)

    def generate_speaker_replay_spoof(self, original_signal: np.ndarray) -> np.ndarray:
        """
        Simulates an Adversarial Attack: A technician trying to trick the post-repair test
        by playing a recorded healthy audio file from a smartphone speaker:
        - Electro-acoustic high-pass filter: Cuts off physical structural vibration < 180 Hz (< 0.01x)
        - Smartphone speaker enclosure resonance peak around 3.2 kHz (Q ~ 3.5)
        - DAC digital quantization noise floor across 6 kHz - 20 kHz with high spectral flatness
        """
        fft_data = np.fft.rfft(original_signal)
        freqs = np.fft.rfftfreq(len(original_signal), 1.0 / self.sample_rate)
        
        # 1. Attenuate physical low frequencies below 180 Hz (smartphone transducer limit)
        fft_data[freqs < 180.0] *= 0.01
        
        # 2. Add smartphone speaker acoustic cavity resonance boost around 3.2 kHz
        speaker_peak = np.exp(-((freqs - 3200.0) ** 2) / (2 * (280.0 ** 2)))
        fft_data *= (1.0 + 1.8 * speaker_peak)
        
        spoofed = np.fft.irfft(fft_data, n=len(original_signal))
        
        # 3. Add DAC digital quantization noise and reconstruction floor
        quant_noise = 0.018 * self.rng.uniform(-1, 1, len(original_signal))
        spoofed = spoofed + quant_noise
        return spoofed / (np.max(np.abs(spoofed)) + 1e-9)

    def add_ambient_noise(self, sig: np.ndarray, snr_db: float = 20.0) -> np.ndarray:
        """
        Adds realistic ambient background noise to a signal to achieve a target SNR (dB).
        """
        sig_power = np.mean(sig ** 2)
        noise_power = sig_power / (10 ** (snr_db / 10.0))
        noise = self.rng.normal(0, np.sqrt(noise_power), len(sig))
        noisy_signal = sig + noise
        return noisy_signal / (np.max(np.abs(noisy_signal)) + 1e-9)
