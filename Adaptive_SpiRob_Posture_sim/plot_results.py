import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("figures", exist_ok=True)


try:
    df = pd.read_csv("results/example_timeseries.csv")
    time = df["time_s"].to_numpy()

    cue_times = df.loc[df["cue_triggered"] == True, "time_s"].to_numpy()

    plt.figure(figsize=(12, 5))
    plt.plot(time, df["pitch_error_deg"].to_numpy(), label="Pitch error")
    plt.plot(time, df["roll_error_deg"].to_numpy(), label="Roll error")
    plt.plot(time, df["upper_error_deg"].to_numpy(), label="Upper error")
    plt.plot(time, df["lower_error_deg"].to_numpy(), label="Lower error")

    for cue_time in cue_times:
        plt.axvline(cue_time, linestyle="--", alpha=0.25)

    plt.xlabel("Time (s)")
    plt.ylabel("Posture error (deg)")
    plt.title("Posture Errors Over Time With Cue Events")
    plt.legend()
    plt.tight_layout()
    plt.savefig("figures/posture_timeseries_with_cues.png", dpi=200)
    plt.close()

    pressure_cols = [
        c for c in df.columns
        if c.startswith("chamber_") and c.endswith("_pressure_kpa")
    ]

    plt.figure(figsize=(12, 5))
    for c in pressure_cols:
        plt.plot(time, df[c].to_numpy(), label=c.replace("_pressure_kpa", ""))

    plt.xlabel("Time (s)")
    plt.ylabel("Pressure (kPa)")
    plt.title("Continuous Chamber Pressure Dynamics")
    plt.legend()
    plt.tight_layout()
    plt.savefig("figures/chamber_pressure_dynamics.png", dpi=200)
    plt.close()

    pressure_matrix = df[pressure_cols].to_numpy().T

    plt.figure(figsize=(12, 4))
    plt.imshow(
        pressure_matrix,
        aspect="auto",
        origin="lower",
        extent=[time.min(), time.max(), 1, len(pressure_cols)]
    )
    plt.colorbar(label="Pressure (kPa)")
    plt.xlabel("Time (s)")
    plt.ylabel("Chamber index")
    plt.title("Chamber Pressure Heatmap")
    plt.tight_layout()
    plt.savefig("figures/chamber_pressure_heatmap.png", dpi=200)
    plt.close()

except FileNotFoundError:
    print("Missing results/example_timeseries.csv. Run evaluate_system.py first.")


try:
    sweep = pd.read_csv("results/controller_sweep_results.csv")
    top = sweep.sort_values("overall_score_lower_is_better").head(10).copy()

    labels = [
        f"T{r.threshold_deg}-D{r.cue_delay_s}-C{r.cooldown_s}-S{r.cue_strength}-{r.base_pattern}"
        for r in top.itertuples()
    ]

    plt.figure(figsize=(12, 5))
    plt.bar(
        range(len(top)),
        top["overall_score_lower_is_better"].to_numpy()
    )
    plt.xticks(
        range(len(top)),
        labels,
        rotation=45,
        ha="right"
    )
    plt.ylabel("Normalized weighted score")
    plt.title("Top 10 Controller Settings")
    plt.tight_layout()
    plt.savefig("figures/controller_sweep_top10.png", dpi=200)
    plt.close()

except FileNotFoundError:
    print("Missing results/controller_sweep_results.csv. Run parameter_sweep.py first.")