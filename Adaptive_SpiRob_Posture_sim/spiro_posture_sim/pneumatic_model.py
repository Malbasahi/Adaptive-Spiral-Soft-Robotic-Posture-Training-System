import numpy as np


class MultiChamberPressureModel:
    def __init__(
        self,
        n_chambers=4,
        dt=0.1,
        k_inflate=1.2,
        k_vent=1.8,
        k_leak=0.03,
        max_pressure_kpa=20.0
    ):
        self.n_chambers = n_chambers
        self.dt = dt
        self.k_inflate = k_inflate
        self.k_vent = k_vent
        self.k_leak = k_leak
        self.max_pressure_kpa = max_pressure_kpa
        self.pressures = np.zeros(n_chambers)

    def step(self, target_pressures):
        target_pressures = np.asarray(target_pressures)

        for i in range(self.n_chambers):
            P = self.pressures[i]
            target = target_pressures[i]

            if target > P:
                dP = self.k_inflate * (target - P) - self.k_leak * P
            elif target < P:
                dP = -self.k_vent * (P - target) - self.k_leak * P
            else:
                dP = -self.k_leak * P

            self.pressures[i] += dP * self.dt
            self.pressures[i] = np.clip(self.pressures[i], 0, self.max_pressure_kpa)

        return self.pressures.copy()


def pressure_to_cue_intensity(pressure_kpa, max_pressure_kpa=20.0):
    pressure_kpa = np.asarray(pressure_kpa)
    return 1.0 - np.exp(-3.0 * pressure_kpa / max_pressure_kpa)