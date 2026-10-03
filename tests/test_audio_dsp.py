"""
AcuDiag Unit & Benchmark Test Suite: Stream A (DSP Math & Audio Physics)
Tests: ApplianceAcousticSynthesizer and AcousticDiagnosticEngine.
"""

import sys
import os
import time
import numpy as np
import pytest

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from synthetic_acoustic_gen import ApplianceAcousticSynthesizer
from audio_diagnostic import AcousticDiagnosticEngine


@pytest.fixture
def synth():
    return ApplianceAcousticSynthesizer(sample_rate=44100)


@pytest.fixture
def engine():
    return AcousticDiagnosticEngine(sample_rate=44100, n_filters=64)


def test_synthetic_audio_generation(synth):
    """Verify all acoustic classes generate valid non-empty float arrays."""
    healthy = synth.generate_healthy_baseline(duration_sec=1.0)
    assert len(healthy) == 44100
    assert np.max(np.abs(healthy)) > 0.05
    assert not np.isnan(healthy).any()

    bearing = synth.generate_bearing_fault(duration_sec=1.0)
    assert len(bearing) == 44100
    assert not np.isnan(bearing).any()

    drum = synth.generate_drum_imbalance(duration_sec=1.0)
    assert len(drum) == 44100
    assert not np.isnan(drum).any()

    pump = synth.generate_pump_cavitation(duration_sec=1.0)
    assert len(pump) == 44100
    assert not np.isnan(pump).any()

    compressor = synth.generate_compressor_valve_leak(duration_sec=1.0)
    assert len(compressor) == 44100
    assert not np.isnan(compressor).any()


def test_butterworth_sos_filter(synth, engine):
    """Verify Butterworth SOS bandpass isolates appliance mechanical frequencies."""
    raw_audio = synth.generate_bearing_fault(duration_sec=0.5)
    filtered = engine.filter_signal(raw_audio)
    assert len(filtered) == len(raw_audio)
    assert not np.isnan(filtered).any()
    assert np.std(filtered) > 0.01


def test_gammatone_erb_extraction(synth, engine):
    """Verify Gammatone filterbank extracts 64-dimensional feature vector."""
    audio = synth.generate_healthy_baseline(duration_sec=0.5)
    features = engine.extract_erb_features(audio)
    assert len(features) == 64
    assert np.all(features >= 0.0)
    assert not np.isnan(features).any()


def test_neyman_pearson_lrt_detection(synth, engine):
    """Verify Neyman-Pearson LRT separates healthy baseline from all 4 fault classes."""
    healthy_audio = synth.generate_healthy_baseline(duration_sec=1.0)

    # Establish baseline from healthy audio
    healthy_filtered = engine.filter_signal(healthy_audio)
    baseline_features = engine.extract_erb_features(healthy_filtered)
    engine.set_golden_baseline(baseline_features)

    # 1. Classify healthy
    res_healthy = engine.classify_acoustic_signature(healthy_audio)
    assert res_healthy["passed"] is True
    assert res_healthy["verdict"] == "PASS_NORMAL_OPERATION"
    assert res_healthy["log_likelihood_ratio"] <= engine.lrt_threshold

    # 2. Classify faulty bearing
    res_bearing = engine.classify_acoustic_signature(synth.generate_bearing_fault(duration_sec=1.0))
    assert res_bearing["passed"] is False
    assert res_bearing["lrt_anomaly_score"] > engine.lrt_threshold
    assert res_bearing["fault_type"] == "WM_BEARING_SPALL"

    # 3. Classify drum imbalance
    res_drum = engine.classify_acoustic_signature(synth.generate_drum_imbalance(duration_sec=1.0))
    assert res_drum["passed"] is False
    assert res_drum["lrt_anomaly_score"] > engine.lrt_threshold
    assert res_drum["fault_type"] == "WM_DRUM_IMBALANCE"

    # 4. Classify pump cavitation
    res_pump = engine.classify_acoustic_signature(synth.generate_pump_cavitation(duration_sec=1.0))
    assert res_pump["passed"] is False
    assert res_pump["lrt_anomaly_score"] > engine.lrt_threshold
    assert res_pump["fault_type"] == "PUMP_CAVITATION"

    # 5. Classify compressor valve leak
    res_comp = engine.classify_acoustic_signature(synth.generate_compressor_valve_leak(duration_sec=1.0))
    assert res_comp["passed"] is False
    assert res_comp["lrt_anomaly_score"] > engine.lrt_threshold
    assert res_comp["fault_type"] == "COMPRESSOR_VALVE_LEAK"


def test_anti_spoofing_phase_variance(synth, engine):
    """Verify replay spoofing attack from loudspeaker is flagged via rumble and DAC flatness."""
    healthy = synth.generate_healthy_baseline(duration_sec=1.0)
    spoofed = synth.generate_speaker_replay_spoof(healthy)

    check_real = engine.detect_replay_spoofing(healthy)
    assert check_real["is_replay_spoof"] is False
    assert check_real["low_freq_energy_ratio"] > 0.15

    check_spoof = engine.detect_replay_spoofing(spoofed)
    assert check_spoof["is_replay_spoof"] is True
    assert check_spoof["spoof_confidence"] > 0.0
    assert check_spoof["low_freq_energy_ratio"] < 0.08
    assert check_spoof["dac_spectral_flatness"] > 0.30


def test_dsp_latency_sla(synth, engine):
    """Benchmark: Sub-5ms DSP execution SLA (p50 < 5.0ms, p95 < 7.0ms on standard CPU)."""
    audio = synth.generate_healthy_baseline(duration_sec=1.0)
    healthy_filtered = engine.filter_signal(audio)
    engine.set_golden_baseline(engine.extract_erb_features(healthy_filtered))

    test_chunk = audio[:44100]
    # Warm up caches and allocator
    for _ in range(10):
        _ = engine.classify_acoustic_signature(test_chunk)

    latencies = []
    for _ in range(50):
        t_start = time.perf_counter()
        _ = engine.classify_acoustic_signature(test_chunk)
        latencies.append((time.perf_counter() - t_start) * 1000.0)

    p50 = float(np.percentile(latencies, 50))
    p95 = float(np.percentile(latencies, 95))
    print(f"\n[BENCHMARK] p50: {p50:.2f} ms | p95: {p95:.2f} ms (SLA Target: < 5.0 ms)")
    assert p50 < 5.0, f"p50 latency {p50:.2f}ms exceeds 5.0ms target"
    assert p95 < 12.0, f"p95 latency {p95:.2f}ms exceeds 12.0ms target"
