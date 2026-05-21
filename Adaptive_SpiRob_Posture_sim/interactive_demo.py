import sys
import pygame
import numpy as np

from spiro_posture_sim.pneumatic_model import (
    MultiChamberPressureModel,
    pressure_to_cue_intensity
)

pygame.init()

# ============================================================
# Window and visual style
# ============================================================

WIDTH, HEIGHT = 1280, 820
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Interactive Soft Robotic Posture Training Simulation")

clock = pygame.time.Clock()

FONT = pygame.font.SysFont("Arial", 18)
SMALL = pygame.font.SysFont("Arial", 15)
TITLE = pygame.font.SysFont("Arial", 28, bold=True)
HEADER = pygame.font.SysFont("Arial", 22, bold=True)
BIG = pygame.font.SysFont("Arial", 34, bold=True)

BG = (244, 244, 240)
PANEL = (255, 255, 252)
BORDER = (205, 205, 195)
TEXT = (25, 30, 35)
MUTED = (105, 110, 115)
GREEN = (20, 140, 80)
RED = (190, 70, 55)
BLUE = (30, 110, 190)
TEAL = (25, 150, 150)
PURPLE = (130, 90, 170)
ORANGE = (230, 135, 40)
DARK = (35, 35, 35)
LIGHT_GREY = (230, 230, 225)

CHAMBER_COLORS = [BLUE, TEAL, PURPLE, ORANGE]

# ============================================================
# Simulation parameters
# ============================================================

dt = 0.05
n_chambers = 4
max_pressure_kpa = 20.0
threshold_deg = 7.0
cue_strength = 1.3
controller_enabled = True

pitch_error = 0.0
roll_error = 0.0
upper_error = 0.0
lower_error = 0.0

pressure_model = MultiChamberPressureModel(
    n_chambers=n_chambers,
    dt=dt,
    max_pressure_kpa=max_pressure_kpa
)

# ============================================================
# Helper functions
# ============================================================

def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def draw_text(text, x, y, color=TEXT, font_obj=None):
    if font_obj is None:
        font_obj = FONT

    surface = font_obj.render(str(text), True, color)
    screen.blit(surface, (int(x), int(y)))


def draw_centered_text(text, rect, color=TEXT, font_obj=None):
    if font_obj is None:
        font_obj = FONT

    surface = font_obj.render(str(text), True, color)
    x = rect.x + (rect.w - surface.get_width()) // 2
    y = rect.y + (rect.h - surface.get_height()) // 2
    screen.blit(surface, (x, y))


def draw_panel(rect, title=None):
    pygame.draw.rect(screen, PANEL, rect, border_radius=14)
    pygame.draw.rect(screen, BORDER, rect, width=1, border_radius=14)

    if title:
        draw_text(title, rect.x + 20, rect.y + 16, color=TEXT, font_obj=HEADER)


def draw_button_label(key, description, x, y, color=BLUE):
    key_rect = pygame.Rect(x, y, 72, 32)
    pygame.draw.rect(screen, color, key_rect, border_radius=7)
    draw_centered_text(key, key_rect, color=(255, 255, 255), font_obj=SMALL)
    draw_text(description, x + 90, y + 6, color=TEXT, font_obj=FONT)


def draw_value_row(label, value, x, y, value_color=TEXT):
    draw_text(label, x, y, color=MUTED, font_obj=FONT)
    draw_text(value, x + 185, y, color=value_color, font_obj=FONT)


def detect_mode(pitch, roll, upper, lower):
    if pitch > threshold_deg:
        return "forward slouch"
    if roll > threshold_deg:
        return "right lean"
    if roll < -threshold_deg:
        return "left lean"
    if upper > threshold_deg:
        return "upper rounding"
    if lower > threshold_deg:
        return "lower collapse"
    return "neutral"


def select_chambers(mode):
    mapping = {
        "forward slouch": [1, 2],
        "left lean": [0],
        "right lean": [3],
        "upper rounding": [2],
        "lower collapse": [1],
        "neutral": []
    }
    return mapping.get(mode, [])


def build_target_pressure(active_chambers):
    target = np.zeros(n_chambers)

    for chamber in active_chambers:
        target[chamber] = cue_strength * max_pressure_kpa

    return target


# ============================================================
# Drawing functions
# ============================================================

def draw_header():
    header_rect = pygame.Rect(0, 0, WIDTH, 56)
    pygame.draw.rect(screen, (28, 43, 60), header_rect)

    draw_centered_text(
        "INTERACTIVE SOFT ROBOTIC POSTURE TRAINING SIMULATION",
        header_rect,
        color=(255, 255, 255),
        font_obj=TITLE
    )

    live_rect = pygame.Rect(WIDTH - 120, 14, 85, 28)
    pygame.draw.rect(screen, GREEN, live_rect, border_radius=14)
    draw_centered_text("LIVE", live_rect, color=(255, 255, 255), font_obj=SMALL)


def draw_status_banner(mode):
    banner = pygame.Rect(365, 96, 550, 65)

    if mode == "neutral":
        color = GREEN
        text = "POSTURE ACCEPTABLE"
    else:
        color = RED
        text = "POSTURE ERROR DETECTED"

    draw_centered_text(text, banner, color=color, font_obj=BIG)


def draw_controls_panel():
    panel = pygame.Rect(24, 96, 315, 560)
    draw_panel(panel, "Keyboard Controls")

    y = 155
    draw_button_label("UP", "Forward slouch", 50, y)
    draw_button_label("LEFT", "Left lean", 50, y + 45)
    draw_button_label("RIGHT", "Right lean", 50, y + 90)
    draw_button_label("W", "Upper rounding", 50, y + 135)
    draw_button_label("S", "Lower collapse", 50, y + 180)
    draw_button_label("SPACE", "Toggle controller", 50, y + 225, color=GREEN)
    draw_button_label("R", "Reset posture", 50, y + 270, color=ORANGE)
    draw_button_label("Q/ESC", "Quit simulation", 50, y + 315, color=RED)

    legend_box = pygame.Rect(42, 540, 255, 82)
    pygame.draw.rect(screen, (250, 250, 247), legend_box, border_radius=10)
    pygame.draw.rect(screen, BORDER, legend_box, width=1, border_radius=10)

    draw_text("Chamber Legend", 55, 550, font_obj=SMALL)

    labels = [
        ("C1", "lower-left"),
        ("C2", "lower-right"),
        ("C3", "upper-left"),
        ("C4", "upper-right")
    ]

    col_1_x = 58
    col_2_x = 175
    row_1_y = 582
    row_2_y = 607

    positions = [
        (col_1_x, row_1_y),
        (col_2_x, row_1_y),
        (col_1_x, row_2_y),
        (col_2_x, row_2_y)
    ]

    for i, ((code, name), (x, y_pos)) in enumerate(zip(labels, positions)):
        pygame.draw.circle(screen, CHAMBER_COLORS[i], (x, y_pos + 7), 8)
        draw_text(code, x + 14, y_pos, font_obj=SMALL)
        draw_text(name, x + 38, y_pos, color=MUTED, font_obj=SMALL)

def draw_system_panel(mode, active_chambers, pressures, cue_intensity):
    panel = pygame.Rect(940, 96, 315, 520)
    draw_panel(panel, "System State")

    x = panel.x + 25
    y = panel.y + 70

    state_color = GREEN if controller_enabled else RED

    draw_value_row("Controller", "ON" if controller_enabled else "OFF", x, y, state_color)
    draw_value_row("Detected posture", mode, x, y + 34, GREEN if mode == "neutral" else RED)
    draw_value_row("Active chambers", str([c + 1 for c in active_chambers]), x, y + 68)
    draw_value_row("Mean pressure", f"{np.mean(pressures):.2f} kPa", x, y + 102)
    draw_value_row("Mean cue", f"{np.mean(cue_intensity):.2f}", x, y + 136)

    pygame.draw.line(screen, LIGHT_GREY, (x, y + 182), (panel.right - 25, y + 182), 2)

    draw_text("IMU Measurements", x, y + 215, font_obj=HEADER)
    draw_value_row("Pitch error", f"{pitch_error:.2f} deg", x, y + 260, BLUE)
    draw_value_row("Roll error", f"{roll_error:.2f} deg", x, y + 294, TEAL)
    draw_value_row("Upper error", f"{upper_error:.2f} deg", x, y + 328, PURPLE)
    draw_value_row("Lower error", f"{lower_error:.2f} deg", x, y + 362, ORANGE)


def draw_back_model(pitch, roll, upper, lower, pressures):
    panel = pygame.Rect(365, 180, 550, 436)
    draw_panel(panel)

    center_x = panel.centerx
    base_y = panel.y + 360

    pitch_offset = pitch * 2.4
    roll_offset = roll * 3.0
    upper_offset = upper * 1.8
    lower_offset = lower * 1.5

    pelvis = np.array([center_x, base_y])
    lower_spine = np.array([center_x + roll_offset * 0.35, base_y - 115 + lower_offset])
    upper_spine = np.array([center_x + roll_offset, base_y - 245 + pitch_offset + upper_offset])
    head = np.array([center_x + roll_offset * 1.15, base_y - 320 + pitch_offset + upper_offset])

    pygame.draw.line(
        screen,
        (120, 180, 130),
        (center_x, base_y + 16),
        (center_x, panel.y + 60),
        2
    )

    draw_text("Target upright spine", center_x + 16, panel.y + 62, color=MUTED, font_obj=SMALL)

    pygame.draw.line(screen, DARK, pelvis.astype(int), lower_spine.astype(int), 8)
    pygame.draw.line(screen, DARK, lower_spine.astype(int), upper_spine.astype(int), 8)
    pygame.draw.line(screen, DARK, upper_spine.astype(int), head.astype(int), 8)

    pygame.draw.circle(screen, DARK, pelvis.astype(int), 12)
    pygame.draw.circle(screen, DARK, lower_spine.astype(int), 10)
    pygame.draw.circle(screen, DARK, upper_spine.astype(int), 10)
    pygame.draw.circle(screen, DARK, head.astype(int), 23)

    imu1 = pygame.Rect(upper_spine[0] - 28, upper_spine[1] - 14, 56, 28)
    imu2 = pygame.Rect(lower_spine[0] - 28, lower_spine[1] - 14, 56, 28)

    pygame.draw.rect(screen, BLUE, imu1, border_radius=6)
    pygame.draw.rect(screen, TEAL, imu2, border_radius=6)

    draw_centered_text("IMU-1", imu1, color=(255, 255, 255), font_obj=SMALL)
    draw_centered_text("IMU-2", imu2, color=(255, 255, 255), font_obj=SMALL)

    chamber_positions = [
        np.array([center_x - 110, base_y - 105]),
        np.array([center_x + 110, base_y - 105]),
        np.array([center_x - 115, base_y - 230]),
        np.array([center_x + 115, base_y - 230]),
    ]

    label_offsets = [
        np.array([-75, 25]),
        np.array([35, 25]),
        np.array([-75, -45]),
        np.array([35, -45]),
    ]

    for i, pos in enumerate(chamber_positions):
        pressure = pressures[i]
        intensity = clamp(pressure / max_pressure_kpa, 0.0, 1.0)
        radius = int(24 + 18 * intensity)
        color = CHAMBER_COLORS[i]

        pygame.draw.circle(screen, color, pos.astype(int), radius)
        pygame.draw.circle(screen, DARK, pos.astype(int), radius, 2)

        chamber_label = pygame.Rect(pos[0] - 22, pos[1] - 15, 44, 30)
        draw_centered_text(f"C{i + 1}", chamber_label, color=(255, 255, 255), font_obj=HEADER)

        label_pos = pos + label_offsets[i]
        label_rect = pygame.Rect(label_pos[0], label_pos[1], 82, 28)

        pygame.draw.rect(screen, (255, 255, 255), label_rect, border_radius=8)
        pygame.draw.rect(screen, BORDER, label_rect, width=1, border_radius=8)
        draw_centered_text(f"{pressure:.1f} kPa", label_rect, color=TEXT, font_obj=SMALL)

        pygame.draw.line(
            screen,
            color,
            pos.astype(int),
            (label_rect.centerx, label_rect.centery),
            2
        )


def draw_pressure_panel(pressures, cue_intensity):
    panel = pygame.Rect(24, 640, 1232, 155)
    draw_panel(panel, "Chamber Pressure and Cue Intensity")

    start_x = 58
    y = 700
    block_w = 285

    labels = ["C1 Lower Left", "C2 Lower Right", "C3 Upper Left", "C4 Upper Right"]

    for i in range(n_chambers):
        x = start_x + i * block_w
        color = CHAMBER_COLORS[i]
        pressure = pressures[i]
        intensity = cue_intensity[i]

        tag = pygame.Rect(x, y, 44, 28)
        pygame.draw.rect(screen, color, tag, border_radius=7)
        draw_centered_text(f"C{i + 1}", tag, color=(255, 255, 255), font_obj=SMALL)

        draw_text(labels[i], x + 55, y + 4, font_obj=FONT)

        bar_x = x
        bar_y = y + 50
        bar_w = 210
        bar_h = 14

        pygame.draw.rect(screen, LIGHT_GREY, (bar_x, bar_y, bar_w, bar_h), border_radius=7)

        fill_w = int(bar_w * clamp(pressure / max_pressure_kpa, 0, 1))
        pygame.draw.rect(screen, color, (bar_x, bar_y, fill_w, bar_h), border_radius=7)

        draw_text(
            f"{pressure:.1f} kPa  |  cue {intensity * 100:.0f}%",
            x,
            y + 75,
            font_obj=SMALL
        )


# ============================================================
# Main loop
# ============================================================

running = True

while running:
    screen.fill(BG)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                running = False

            if event.key == pygame.K_SPACE:
                controller_enabled = not controller_enabled

            if event.key == pygame.K_r:
                pitch_error = 0.0
                roll_error = 0.0
                upper_error = 0.0
                lower_error = 0.0
                pressure_model.pressures[:] = 0.0

    if keys[pygame.K_UP]:
        pitch_error += 0.25

    if keys[pygame.K_LEFT]:
        roll_error -= 0.25

    if keys[pygame.K_RIGHT]:
        roll_error += 0.25

    if keys[pygame.K_w]:
        upper_error += 0.25

    if keys[pygame.K_s]:
        lower_error += 0.25

    pitch_error += 0.015
    upper_error += 0.006

    mode = detect_mode(
        pitch_error,
        roll_error,
        upper_error,
        lower_error
    )

    if controller_enabled:
        active_chambers = select_chambers(mode)
        target_pressures = build_target_pressure(active_chambers)
    else:
        active_chambers = []
        target_pressures = np.zeros(n_chambers)

    pressures = pressure_model.step(target_pressures)
    cue_intensity = pressure_to_cue_intensity(pressures, max_pressure_kpa)

    correction_gain = 0.025
    correction = correction_gain * np.mean(cue_intensity)

    if controller_enabled:
        pitch_error -= correction * pitch_error
        roll_error -= correction * roll_error
        upper_error -= correction * upper_error
        lower_error -= correction * lower_error

    pitch_error = clamp(pitch_error, -25, 30)
    roll_error = clamp(roll_error, -25, 25)
    upper_error = clamp(upper_error, -25, 30)
    lower_error = clamp(lower_error, -25, 30)

    draw_header()
    draw_status_banner(mode)
    draw_controls_panel()
    draw_back_model(pitch_error, roll_error, upper_error, lower_error, pressures)
    draw_system_panel(mode, active_chambers, pressures, cue_intensity)
    draw_pressure_panel(pressures, cue_intensity)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()