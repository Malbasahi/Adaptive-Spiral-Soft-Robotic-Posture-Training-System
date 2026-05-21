import numpy as np
import pandas as pd
from shapely.geometry import LineString


def generate_spiral(width_mm=280, height_mm=420, turns=2.0, points=600):
    theta = np.linspace(0, 2 * np.pi * turns, points)
    r_x = width_mm * 0.42 * theta / theta.max()
    r_y = height_mm * 0.42 * theta / theta.max()
    x = r_x * np.cos(theta)
    y = r_y * np.sin(theta)
    return np.column_stack([x, y])


def split_into_chambers(points, n_chambers=4):
    return np.array_split(points, n_chambers)


def estimate_curvature(points):
    x = points[:, 0]
    y = points[:, 1]
    dx = np.gradient(x)
    dy = np.gradient(y)
    ddx = np.gradient(dx)
    ddy = np.gradient(dy)
    return np.abs(dx * ddy - dy * ddx) / np.maximum((dx**2 + dy**2) ** 1.5, 1e-6)


def analyze_design(design_id="A", width_mm=280, height_mm=420, turns=2.0,
                   n_chambers=4, chamber_width_mm=25, seal_width_mm=4):
    spiral = generate_spiral(width_mm, height_mm, turns)
    chambers = split_into_chambers(spiral, n_chambers)
    rows = []
    for i, pts in enumerate(chambers):
        line = LineString(pts)
        chamber_area = line.buffer(chamber_width_mm / 2)
        seal_area = line.buffer(chamber_width_mm / 2 + seal_width_mm)
        curvature = estimate_curvature(pts)
        centroid = chamber_area.centroid
        inlet = pts[0]
        rows.append({
            "design_id": design_id,
            "chamber_id": i + 1,
            "centerline_length_mm": line.length,
            "chamber_area_mm2": chamber_area.area,
            "seal_area_mm2": seal_area.area,
            "centroid_x_mm": centroid.x,
            "centroid_y_mm": centroid.y,
            "mean_curvature": float(np.mean(curvature)),
            "max_curvature": float(np.max(curvature)),
            "distance_from_spine_mm": abs(centroid.x),
            "inlet_x_mm": inlet[0],
            "inlet_y_mm": inlet[1],
        })
    return pd.DataFrame(rows)
