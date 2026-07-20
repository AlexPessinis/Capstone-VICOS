# modules/mock_obd.py

import random

def get_mock_data():
    return {
        "RPM": random.randint(700, 2500),
        "SPEED": random.randint(0, 65),
        "COOLANT_TEMP": random.randint(70, 105),
        "BATTERY_VOLTAGE": round(random.uniform(12.5, 14.2), 2)
    }
