import numpy as np


def cue_intensity_from_error(error_magnitude, cue_strength=1.0, max_error=20.0):
    return min(1.0, error_magnitude / max_error) * cue_strength


def build_cue_command(pattern, chambers, n_chambers, intensity, t_since_cue, pulse_period=1.0):
    commands = {i: 0.0 for i in range(1, n_chambers + 1)}
    if not chambers:
        return commands

    if pattern == "pulse":
        phase = (t_since_cue % pulse_period) / pulse_period
        active = phase < 0.5
        for ch in chambers:
            commands[ch] = intensity if active else 0.0

    elif pattern == "wave":
        idx = int((t_since_cue / pulse_period) * len(chambers)) % len(chambers)
        commands[chambers[idx]] = intensity

    elif pattern == "escalating":
        gain = min(1.5, 0.5 + 0.25 * t_since_cue)
        for ch in chambers:
            commands[ch] = min(1.0, intensity * gain)

    else:
        for ch in chambers:
            commands[ch] = intensity

    return commands


def choose_pattern(bad_posture_duration, base_pattern="pulse"):
    if bad_posture_duration < 3:
        return base_pattern
    if bad_posture_duration < 6:
        return "escalating"
    return "wave"
