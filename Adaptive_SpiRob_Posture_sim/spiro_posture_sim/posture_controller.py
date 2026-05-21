import numpy as np
import pandas as pd

from .pneumatic_model import MultiChamberPressureModel, pressure_to_cue_intensity

def select_chambers(mode, n_chambers=4):
    if n_chambers == 4:
        mapping = {
            "forward_slouch": [1, 2],
            "left_lean": [0],
            "right_lean": [3],
            "upper_thoracic_rounding": [2],
            "lower_back_collapse": [1],
            "neutral": []
        }
    else:
        mapping = {
            "forward_slouch": [2, 3],
            "left_lean": [0, 1],
            "right_lean": [4, 5],
            "upper_thoracic_rounding": [4],
            "lower_back_collapse": [1],
            "neutral": []
        }

    return mapping.get(mode, [])


def detect_posture_mode(pitch, roll, upper, lower, threshold):
    if pitch > threshold:
        return "forward_slouch"
    if roll > threshold:
        return "right_lean"
    if roll < -threshold:
        return "left_lean"
    if upper > threshold:
        return "upper_thoracic_rounding"
    if lower > threshold:
        return "lower_back_collapse"
    return "neutral"


def build_target_pressure(
    active_chambers,
    cue_strength,
    n_chambers,
    max_pressure_kpa=20.0
):
    target = np.zeros(n_chambers)

    for chamber in active_chambers:
        target[chamber] = cue_strength * max_pressure_kpa

    return target


def simulate_posture(
    duration_s=180,
    dt=0.1,
    threshold_deg=7,
    cue_delay_s=0.5,
    cue_cooldown_s=3,
    cue_strength=1.6,
    n_chambers=4,
    base_pattern="wave",
    noise_level=0.08,
    natural_slouch_rate=0.025,
    user_sensitivity=0.38,
    max_pressure_kpa=20.0
):
    time = np.arange(0, duration_s, dt)

    pressure_model = MultiChamberPressureModel(
        n_chambers=n_chambers,
        dt=dt,
        max_pressure_kpa=max_pressure_kpa
    )

    pitch = 0.0
    roll = 0.0
    upper = 0.0
    lower = 0.0

    bad_posture_duration = 0.0
    cooldown_timer = 0.0

    rows = []

    for t in time:
        pitch += natural_slouch_rate + np.random.normal(0, noise_level)
        roll += np.random.normal(0, noise_level * 0.6)
        upper += natural_slouch_rate * 0.6 + np.random.normal(0, noise_level * 0.7)
        lower += np.random.normal(0, noise_level * 0.7)

        mode = detect_posture_mode(
            pitch=pitch,
            roll=roll,
            upper=upper,
            lower=lower,
            threshold=threshold_deg
        )

        poor_posture = mode != "neutral"

        if poor_posture:
            bad_posture_duration += dt
        else:
            bad_posture_duration = 0.0

        if cooldown_timer > 0:
            cooldown_timer -= dt

        cue_triggered = False
        active_chambers = []

        if poor_posture and bad_posture_duration >= cue_delay_s and cooldown_timer <= 0:
            cue_triggered = True
            active_chambers = select_chambers(mode, n_chambers)
            cooldown_timer = cue_cooldown_s

        target_pressures = build_target_pressure(
            active_chambers=active_chambers,
            cue_strength=cue_strength,
            n_chambers=n_chambers,
            max_pressure_kpa=max_pressure_kpa
        )

        pressures = pressure_model.step(target_pressures)
        cue_intensities = pressure_to_cue_intensity(pressures, max_pressure_kpa)

        total_cue = np.mean(cue_intensities)

        correction = user_sensitivity * total_cue

        pitch -= correction * np.sign(pitch) * abs(pitch) * dt
        roll -= correction * np.sign(roll) * abs(roll) * dt
        upper -= correction * np.sign(upper) * abs(upper) * dt
        lower -= correction * np.sign(lower) * abs(lower) * dt

        comfort_penalty = np.sum(pressures / max_pressure_kpa) * dt

        row = {
            "time_s": t,
            "pitch_error_deg": pitch,
            "roll_error_deg": roll,
            "upper_error_deg": upper,
            "lower_error_deg": lower,
            "posture_mode": mode,
            "posture_state": "poor" if poor_posture else "acceptable",
            "cue_triggered": cue_triggered,
            "bad_posture_duration_s": bad_posture_duration,
            "comfort_penalty": comfort_penalty,
            "mean_pressure_kpa": np.mean(pressures),
            "max_pressure_kpa": np.max(pressures),
        }

        for i in range(n_chambers):
            row[f"chamber_{i + 1}_command"] = target_pressures[i] / max_pressure_kpa
            row[f"chamber_{i + 1}_pressure_kpa"] = pressures[i]
            row[f"chamber_{i + 1}_cue_intensity"] = cue_intensities[i]

        rows.append(row)

    return pd.DataFrame(rows)