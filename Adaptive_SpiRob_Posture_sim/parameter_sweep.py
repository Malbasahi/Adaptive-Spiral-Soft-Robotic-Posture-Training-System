import os
import pandas as pd

from spiro_posture_sim.posture_controller import simulate_posture

os.makedirs("results", exist_ok=True)

raw_results = []

for threshold in [5, 6, 7, 8]:
    for delay in [0.5, 1.0, 2.0]:
        for cooldown in [3, 4, 6, 8]:
            for strength in [1.0, 1.3, 1.6]:
                for pattern in ["pulse", "wave"]:

                    df = simulate_posture(
                        threshold_deg=threshold,
                        cue_delay_s=delay,
                        cue_cooldown_s=cooldown,
                        cue_strength=strength,
                        base_pattern=pattern,
                        n_chambers=4
                    )

                    mean_error = (
                        df["pitch_error_deg"].abs().mean()
                        + df["roll_error_deg"].abs().mean()
                        + df["upper_error_deg"].abs().mean()
                        + df["lower_error_deg"].abs().mean()
                    ) / 4

                    raw_results.append({
                        "threshold_deg": threshold,
                        "cue_delay_s": delay,
                        "cooldown_s": cooldown,
                        "cue_strength": strength,
                        "base_pattern": pattern,
                        "mean_error_deg": mean_error,
                        "bad_posture_percent": 100 * (df["posture_state"] == "poor").mean(),
                        "number_of_cues": int(df["cue_triggered"].sum()),
                        "total_comfort_penalty": df["comfort_penalty"].sum(),
                        "mean_pressure_kpa": df["mean_pressure_kpa"].mean(),
                        "max_pressure_kpa": df["max_pressure_kpa"].max(),
                    })

results = pd.DataFrame(raw_results)

for col in [
    "mean_error_deg",
    "bad_posture_percent",
    "number_of_cues",
    "total_comfort_penalty"
]:
    min_val = results[col].min()
    max_val = results[col].max()
    results[f"norm_{col}"] = (results[col] - min_val) / max(max_val - min_val, 1e-9)

results["overall_score_lower_is_better"] = (
    0.45 * results["norm_bad_posture_percent"]
    + 0.25 * results["norm_mean_error_deg"]
    + 0.20 * results["norm_total_comfort_penalty"]
    + 0.10 * results["norm_number_of_cues"]
)

results = results.sort_values("overall_score_lower_is_better")
results.to_csv("results/controller_sweep_results.csv", index=False)

print(results.head(15))