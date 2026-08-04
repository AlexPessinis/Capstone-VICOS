# modules/persistence.py

import json
import os
from datetime import datetime

TRIP_FILE = "trip_data.json"

def load_trip():
    if not os.path.exists(TRIP_FILE):
        return {
            "start_time": None,
            "end_time": None,
            "miles": 0.0,
            "avg_speed": 0.0,
            "max_speed": 0.0,
            "avg_mpg": 0.0,
            "samples": 0
        }

    with open(TRIP_FILE, "r") as f:
        return json.load(f)


def save_trip(trip):
    with open(TRIP_FILE, "w") as f:
        json.dump(trip, f, indent=4)
