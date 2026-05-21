import os
import pandas as pd

from spiro_posture_sim.geometry_model import analyze_design
from spiro_posture_sim.posture_controller import simulate_posture

os.makedirs("results", exist_ok=True)


designs = [
    {
        "design_id": "A",
        "width_mm": 280,
        "height_mm": 420,
        "turns": 2.0,
        "n_chambers": 4,
        "chamber_width_mm": 25
    },
    {
        "design_id": "B",
        "width_mm": 280,
        "height_mm": 420,
        "turns": 1.5,
        "n_chambers": 4,
        "chamber_width_mm": 30
    },
    {
        "design_id": "C",
        "width_mm": 280,
        "height_mm": 420,
        "turns": 2.5,
        "n_chambers": 6,
        "chamber_width_mm": 20
    }
]


all_geometry = []
system_summary = []

for design in designs:
    geometry_df = analyze_design(**design)
    all_geometry.append(geometry_df)

    posture_df = simulate_posture(
        threshold_deg=7,
        cue_delay_s=0.5,
        cue_cooldown_s=3,
        cue_strength=1.6,
        n_chambers=design["n_chambers"],
        base_pattern="wave"
    )

    mean_error = (
        posture_df["pitch_error_deg"].abs().mean()
        + posture_df["roll_error_deg"].abs().mean()
        + posture_df["upper_error_deg"].abs().mean()
        + posture_df["lower_error_deg"].abs().mean()
    ) / 4

    bad_posture_percent = 100 * (
        posture_df["posture_state"] == "poor"
    ).mean()

    number_of_cues = int(posture_df["cue_triggered"].sum())
    total_comfort_penalty = posture_df["comfort_penalty"].sum()

    overall_score = (
        0.45 * bad_posture_percent / 100
        + 0.25 * mean_error / 10
        + 0.20 * total_comfort_penalty / 100
        + 0.10 * number_of_cues / 100
    )

    system_summary.append({
        "design_id": design["design_id"],
        "n_chambers": design["n_chambers"],
        "turns": design["turns"],
        "chamber_width_mm": design["chamber_width_mm"],
        "mean_error_deg": mean_error,
        "bad_posture_percent": bad_posture_percent,
        "number_of_cues": number_of_cues,
        "total_comfort_penalty": total_comfort_penalty,
        "mean_pressure_kpa": posture_df["mean_pressure_kpa"].mean(),
        "max_pressure_kpa": posture_df["max_pressure_kpa"].max(),
        "mean_chamber_length_mm": geometry_df["centerline_length_mm"].mean(),
        "length_balance_std_mm": geometry_df["centerline_length_mm"].std(),
        "mean_curvature": geometry_df["mean_curvature"].mean(),
        "max_curvature": geometry_df["max_curvature"].max(),
        "overall_score_lower_is_better": overall_score
    })

    if design["design_id"] == "B":
        posture_df.to_csv("results/example_timeseries.csv", index=False)


geometry_results = pd.concat(all_geometry, ignore_index=True)
system_results = pd.DataFrame(system_summary)

geometry_results.to_csv("results/geometry_results.csv", index=False)
system_results.to_csv("results/system_evaluation_results.csv", index=False)

print(system_results)