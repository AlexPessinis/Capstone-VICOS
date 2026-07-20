# ui/dashboard.py

def render_dashboard(data):
    print(f"RPM: {data['RPM']} | Speed: {data['SPEED']} | Coolant: {data['COOLANT_TEMP']} | Voltage: {data['BATTERY_VOLTAGE']}")
