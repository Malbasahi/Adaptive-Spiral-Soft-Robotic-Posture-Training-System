
def comfort_penalty(cue_strength, active_chamber_count, cue_duration_s, pressure_kpa,
                    pressure_limit_kpa=25):
    pressure_ratio = max(0.0, pressure_kpa / pressure_limit_kpa)
    spatial_load = active_chamber_count
    return cue_strength * spatial_load * cue_duration_s * pressure_ratio


def overall_score(mean_error_deg, bad_posture_percent, cue_count, total_comfort_penalty,
                  w_error=1.0, w_bad=0.08, w_cues=0.05, w_comfort=0.2):
    return (
        w_error * mean_error_deg +
        w_bad * bad_posture_percent +
        w_cues * cue_count +
        w_comfort * total_comfort_penalty
    )
