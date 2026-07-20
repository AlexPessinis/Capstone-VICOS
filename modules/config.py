# modules/config.py

OBD_PIDS = {
    "RPM": "010C",
    "SPEED": "010D",
    "COOLANT_TEMP": "0105",
    "BATTERY_VOLTAGE": "0142"
}

TELEMETRY_INTERVAL = 0.5  # seconds
LOGGING_ENABLED = True
