import numpy as np

POSTURE_MODES = [
    "neutral",
    "forward_slouch",
    "left_lean",
    "right_lean",
    "upper_thoracic_rounding",
    "lower_back_collapse",
]


def classify_posture(pitch_error, roll_error, upper_error, lower_error,
                     pitch_threshold=7, roll_threshold=6, segment_threshold=5):
    if upper_error > segment_threshold and upper_error >= lower_error:
        return "upper_thoracic_rounding"
    if lower_error > segment_threshold and lower_error > upper_error:
        return "lower_back_collapse"
    if pitch_error > pitch_threshold:
        return "forward_slouch"
    if roll_error > roll_threshold:
        return "right_lean"
    if roll_error < -roll_threshold:
        return "left_lean"
    return "neutral"


def generate_posture_drift(mode, dt, rng, slouch_rate=0.025, noise_level=0.08):
    pitch = rng.normal(0, noise_level)
    roll = rng.normal(0, noise_level * 0.6)
    upper = rng.normal(0, noise_level * 0.7)
    lower = rng.normal(0, noise_level * 0.7)

    if mode == "forward_slouch":
        pitch += slouch_rate * dt * 10
        upper += slouch_rate * dt * 5
    elif mode == "left_lean":
        roll -= slouch_rate * dt * 8
    elif mode == "right_lean":
        roll += slouch_rate * dt * 8
    elif mode == "upper_thoracic_rounding":
        upper += slouch_rate * dt * 10
        pitch += slouch_rate * dt * 4
    elif mode == "lower_back_collapse":
        lower += slouch_rate * dt * 10
        pitch += slouch_rate * dt * 3

    return pitch, roll, upper, lower


def sample_mode_schedule(time_s):
    cycle = int(time_s // 30) % 5
    return [
        "forward_slouch",
        "left_lean",
        "right_lean",
        "upper_thoracic_rounding",
        "lower_back_collapse",
    ][cycle]
