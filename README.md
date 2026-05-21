# Adaptive Spiral Soft Robotic Posture Training System

Computational framework and interactive digital twin for a wearable soft robotic posture-training system using distributed spiral pneumatic actuation and IMU-based posture sensing.

---

# Overview

This project presents an initial computational prototype for an:

**Adaptive Spiral Soft Robotic Posture Training System for Spine Alignment and Rehabilitation** 

The system is designed to:

* detect trunk posture deviations,
* estimate posture using simulated IMU sensing,
* activate distributed spiral pneumatic chambers,
* and provide corrective soft cues for posture self-correction.

The project combines:

* geometry generation,
* posture simulation,
* pneumatic pressure modeling,
* controller optimization,
* visualization,
* and an interactive real-time digital twin.

---

# Main Features

## Spiral Soft Robotic Garment Simulation

* Parametric spiral chamber geometry
* Multi-chamber distributed actuation
* Spatial cue encoding along the spine

## Posture Estimation

Simulated IMU-based posture monitoring:

* pitch deviation
* roll deviation
* upper thoracic deviation
* lower trunk deviation

## Pneumatic Pressure Dynamics

Continuous pressure simulation:

* inflation
* pressure rise and decay
* leakage behavior
* cue intensity generation

## Controller and Cue Logic

Rule-based controller with:

* posture classification
* chamber selection
* pressure command generation
* pulse and wave cue patterns

## Parameter Sweep and Optimization

Automatic evaluation of:

* posture thresholds
* cue delays
* cooldown timing
* cue intensity
* cue patterns

## Interactive Digital Twin

Real-time simulation environment showing:

* live posture sensing
* chamber activation
* pressure dynamics
* posture correction behavior

---

# Project Structure

```text
spiro_posture_sim_v2/
│
├── spiro_posture_sim/
│   ├── geometry_model.py
│   ├── pneumatic_model.py
│   ├── posture_controller.py
│
├── evaluate_system.py
├── parameter_sweep.py
├── plot_results.py
├── interactive_demo.py
├── run_all.py
│
├── results/
├── figures/
└── README.md
```

---

# Installation

## Clone repository

```bash
git clone <repository-link>
cd Adaptive_SpiRob_Posture_sim
```

## Install dependencies

```bash
pip install numpy scipy pandas matplotlib shapely pygame
```

---

# Running the Simulations

## Run the complete simulation pipeline

```bash
python3 run_all.py
```

This generates:

* geometry analysis
* posture simulation
* controller sweep
* pressure dynamics
* figures and plots

---

# Running the Interactive Digital Twin

```bash
python3 interactive_demo.py
```

The simulation provides:

* live posture visualization
* IMU measurements
* chamber inflation behavior
* pressure dynamics
* controller feedback

---

# Keyboard Controls

| Key     | Action            |
| ------- | ----------------- |
| UP      | Forward slouch    |
| LEFT    | Left lean         |
| RIGHT   | Right lean        |
| W       | Upper rounding    |
| S       | Lower collapse    |
| SPACE   | Toggle controller |
| R       | Reset posture     |
| Q / ESC | Quit simulation   |

---

# Generated Outputs

## Results Folder

```text
results/
├── geometry_results.csv
├── system_evaluation_results.csv
├── controller_sweep_results.csv
├── example_timeseries.csv
```

---

## Figures Folder

```text
figures/
├── posture_timeseries_with_cues.png
├── chamber_pressure_dynamics.png
├── chamber_pressure_heatmap.png
├── controller_sweep_top10.png
```

---

# Simulation Results

## Geometry Evaluation

Three spiral geometries were evaluated computationally.

### Selected Initial Design

* 4 chambers
* 1.5 spiral turns
* 30 mm chamber width

This configuration achieved:

* lower curvature concentration
* improved chamber balance
* better manufacturability

---

## Controller Optimization

A parameter sweep evaluated:

* posture threshold
* cue delay
* cooldown timing
* cue intensity
* pulse/wave patterns

Best-performing configurations were concentrated around:

* threshold = 7–8°
* cue delay = 0.5–1.0 s
* cooldown = 4–6 s
* cue strength = 1.0–1.3

---

## Pneumatic Pressure Dynamics

The pressure model demonstrated:

* stable inflation behavior
* repeatable pressure decay
* localized chamber activation
* continuous soft cue generation

---

## Interactive Digital Twin

The real-time simulation validates:

* posture sensing
* distributed chamber activation
* controller logic
* soft cue response
* posture correction behavior

---

# Current Development Stage

This project currently represents a:

## Computational Soft Robotic System Prototype

The work has progressed beyond conceptual sketches into:

* system-level computational design,
* posture-control simulation,
* pneumatic actuation modeling,
* and interactive visualization.

---

# Future Work

Planned next stages include:

* physical spiral actuator fabrication
* hardware integration
* real IMU sensing
* experimental posture trials
* actuator characterization
* adaptive personalization
* comparison against vibration-based posture systems

---

# Research Motivation

Conventional posture systems typically rely on:

* binary vibration alerts,
* simple tactile feedback,
* or passive mechanical support.

This project investigates whether:

> distributed spiral soft robotic cues can provide more natural and effective posture guidance.

The long-term goal is to develop a wearable soft robotic system capable of:

* posture correction,
* posture training,
* and long-term posture retention improvement.
