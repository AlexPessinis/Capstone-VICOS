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


from collections import deque


class Smoother:
    def __init__(self):
        self.last_values = {}
        self.alpha = {
            "rpm": 0.25,
            "coolant": 0.05,
            "speed": 0.20,
            "iat": 0.10,
            "maf": 0.15,
            "fuel_level": 0.05,
            "mpg": 0.08,
        }
        self.buffers = {key: deque(maxlen=10) for key in self.alpha.keys()}

    def exponential(self, key, new_value):
        """
        Exponential smoothing (EMA).
        key: telemetry field name
        new_value: raw value from OBD-II
        """
        if new_value is None:
            return self.last_values.get(key)

        a = self.alpha.get(key, 0.15)

        if key not in self.last_values:
            self.last_values[key] = new_value
            return new_value

        last = self.last_values[key]
        smoothed = (a * new_value) + ((1 - a) * last)
        self.last_values[key] = smoothed
        return smoothed

    def smooth(self, data, method="ema"):
        smoothed = {}
        for key, value in data.items():
            if method == "ema":
                smoothed[key] = self.exponential(key, value)
            else:
                smoothed[key] = value
        return smoothed


