
def map_posture_to_chambers(posture_mode, n_chambers=4):
    if n_chambers == 4:
        mapping = {
            "neutral": [],
            "forward_slouch": [2, 3],
            "left_lean": [1, 2],
            "right_lean": [3, 4],
            "upper_thoracic_rounding": [3, 4],
            "lower_back_collapse": [1, 2],
        }
    elif n_chambers == 6:
        mapping = {
            "neutral": [],
            "forward_slouch": [3, 4],
            "left_lean": [1, 2, 3],
            "right_lean": [4, 5, 6],
            "upper_thoracic_rounding": [5, 6],
            "lower_back_collapse": [1, 2],
        }
    else:
        mid = max(1, n_chambers // 2)
        mapping = {
            "neutral": [],
            "forward_slouch": [mid, min(n_chambers, mid + 1)],
            "left_lean": list(range(1, mid + 1)),
            "right_lean": list(range(mid + 1, n_chambers + 1)),
            "upper_thoracic_rounding": list(range(mid + 1, n_chambers + 1)),
            "lower_back_collapse": list(range(1, mid + 1)),
        }
    return mapping.get(posture_mode, [])
