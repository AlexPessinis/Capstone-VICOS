# modules/telemetry.py
#
# VICOS Telemetry Module
# ----------------------
# Responsible for:
# - Connecting to the OBD-II adapter
# - Querying core vehicle data (RPM, coolant temp, speed, intake temp, MAF, fuel level)
# - Computing instantaneous MPG (THIS IS APPROXIMATE, DO NOT FULLY RELY)
# - Passing data to the database layer for logging
#
# Smoothing is applied externally via modules/smoothing.py.

import time
import obd

from modules.database import insert_telemetry, init_db
from modules.smoothing import Smoother

# 20 Hz sampling
TELEMETRY_INTERVAL = 0.05  # seconds


# Constants for MPG calculation, based on industry standards for things like
# stoichiometric ratio and the combustion equation. IF YOU RUN LEAN OR RICH, you *MUST*
# CHANGE THESE VALUES!
STOICH_RATIO = 14.7
FUEL_DENSITY_G_PER_ML = 0.745
ML_PER_LITER = 1000.0
LITERS_PER_GALLON = 3.78541


class Telemetry:
    def __init__(self):
        """
        Initialize OBD-II connection and database.
        """
        print("Initializing OBD-II connection...")
        self.connection = obd.OBD()  # auto-connect to USB OBD-II adapter

        print("Initializing database...")
        init_db()

        print("Initializing smoother...")
        self.smoother = Smoother()

    def _get_obd_value(self, command):
        """
        Safely query a single OBD-II command.
        Returns a float value or None if unavailable.
        """
        if not self.connection.is_connected():
            return None

        response = self.connection.query(command)

        if response.is_null():
            return None

        try:
            return float(response.value.magnitude)
        except Exception:
            return None

    def _compute_mpg(self, speed_mph, maf_g_per_s):
        """
        Compute instantaneous MPG using speed and MAF.
        """
        if speed_mph is None or maf_g_per_s is None:
            return None

        if speed_mph <= 0 or maf_g_per_s <= 0:
            return None

        # Convert MAF (g/s) → fuel volume flow (L/hr)
        fuel_ml_per_s = maf_g_per_s / FUEL_DENSITY_G_PER_ML
        fuel_l_per_hr = (fuel_ml_per_s * 3600.0) / ML_PER_LITER

        if fuel_l_per_hr <= 0:
            return None

        fuel_gal_per_hr = fuel_l_per_hr / LITERS_PER_GALLON

        if fuel_gal_per_hr <= 0:
            return None

        mpg = speed_mph / fuel_gal_per_hr

        if mpg < 0 or mpg > 200:
            return None

        return mpg

    def read_raw(self):
        """
        Read raw telemetry values from OBD-II.
        """
        rpm = self._get_obd_value(obd.commands.RPM)
        coolant = self._get_obd_value(obd.commands.COOLANT_TEMP)
        speed = self._get_obd_value(obd.commands.SPEED)
        iat = self._get_obd_value(obd.commands.INTAKE_TEMP)
        maf = self._get_obd_value(obd.commands.MAF)
        fuel_level = self._get_obd_value(obd.commands.FUEL_LEVEL)

        mpg = self._compute_mpg(speed, maf)

        return {
            "rpm": rpm,
            "coolant": coolant,
            "speed": speed,
            "iat": iat,
            "maf": maf,
            "fuel_level": fuel_level,
            "mpg": mpg,
        }

    def telemetry_loop(self):
        """
        Continuous telemetry loop.
        Reads raw data, smooths it, logs it, and prints it.
        """
        print("Starting telemetry loop at 20 Hz...")

        while True:
            raw = self.read_raw()
            smooth = self.smoother.smooth(raw, method="ema")

            insert_telemetry(smooth)

            print(
                f"RPM: {smooth['rpm']} | Coolant: {smooth['coolant']} °C | "
                f"Speed: {smooth['speed']} mph | IAT: {smooth['iat']} °C | "
                f"MAF: {smooth['maf']} g/s | Fuel: {smooth['fuel_level']} % | "
                f"MPG: {smooth['mpg']}"
            )

            time.sleep(TELEMETRY_INTERVAL)


if __name__ == "__main__":
    telemetry = Telemetry()
    telemetry.telemetry_loop()
