# modules/smoothing.py
#
# VICOS Smoothing Algorithms
# --------------------------
# Provides:
# - Exponential smoothing
# - Rolling average smoothing
# - Per-signal smoothing profiles
# - Safe handling of any possible None values
#
# Designed for 20 Hz telemetry sampling. Changing the telemetry sampling
# SHOULD lead to different required smoothing values.

from collections import deque


class Smoother:
    def __init__(self):
        # Store last smoothed values
        self.last_values = {}

        # Per-signal smoothing factors
        self.alpha = {
            "rpm": 0.25,          # fast response due to rapid changes
            "coolant": 0.05,      # bery slow because slow changes
            "speed": 0.20,        # moderate
            "iat": 0.10,          # moderate
            "maf": 0.15,          # moderate
            "fuel_level": 0.05,   # very slow
            "mpg": 0.08,          # also very slow
        }

        # Rolling buffers (completely optional)
        self.buffers = {
            key: deque(maxlen=10) for key in self.alpha.keys()
        }

    def exponential(self, key, new_value):
        """
        Exponential smoothing (EMA).
        key: telemetry field name
        new_value: raw value from OBD-II
        """
        if new_value is None:
            return self.last_values.get(key)

        a = self.alpha.get(key, 0.15)

        # If no previous value, the system should initialize itself
        if key not in self.last_values:
            self.last_values[key] = new_value
            return new_value

        last = self.last_values[key]
        smoothed = (a * new_value) + ((1 - a) * last)

