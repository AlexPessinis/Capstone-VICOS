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
from datetime import datetime

from modules.database import insert_telemetry, init_db
from modules.smoothing import Smoother
from modules.persistence import load_trip, save_trip


TELEMETRY_INTERVAL = 0.05  # 20 Hz

STOICH_RATIO = 14.7
FUEL_DENSITY_G_PER_ML = 0.745
ML_PER_LITER = 1000.0
LITERS_PER_GALLON = 3.78541


class Telemetry:
    def __init__(self):
        print("Initializing OBD-II connection...")

        self.connection = obd.OBD("/dev/ttyUSB0", baudrate=115200, fast=False)
        print("OBD Status:", self.connection.status())

        print("OBD Testing complete.")

        print("Initializing database...")
        init_db()

        print("Initializing smoother...")
        self.smoother = Smoother()

        # Load trip persistence
        self.trip = load_trip()
        self.last_save_time = datetime.now()

        # Ensure required trip keys exist
        self.trip.setdefault("miles", 0.0)
        self.trip.setdefault("max_speed", 0.0)
        self.trip.setdefault("avg_speed", 0.0)
        self.trip.setdefault("avg_mpg", 0.0)
        self.trip.setdefault("samples", 0)
        self.trip.setdefault("fuel_gallons", 0.0)
        self.trip.setdefault("start_time", None)
        self.trip.setdefault("end_time", None)

    def _get_obd_value(self, command):
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
        if speed_mph is None or maf_g_per_s is None:
            return None
        if speed_mph <= 0 or maf_g_per_s <= 0:
            return None

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
        print("Starting telemetry loop at 20 Hz...")

        while True:
            raw = self.read_raw()
            smooth = self.smoother.smooth(raw, method="ema")

            insert_telemetry(smooth)

            # -----------------------------
            # Trip persistence logic
            # -----------------------------
            rpm = smooth["rpm"]
            speed = smooth["speed"]
            mpg = smooth["mpg"]
            maf = smooth["maf"]

            # Start trip when RPM rises
            if rpm is not None and rpm > 1500:
                if self.trip["start_time"] is None:
                    self.trip["start_time"] = datetime.now().isoformat()

            # Save trip data when RPM is low but defined
            if rpm is not None and 0 < rpm < 1200:
                self.trip["end_time"] = datetime.now().isoformat()

                # Miles accumulation (mph → miles/sec)
                if speed is not None and speed > 0:
                    self.trip["miles"] += speed / 3600.0

                    # Max speed
                    self.trip["max_speed"] = max(self.trip["max_speed"], speed)

                # Fuel accumulation (gallons/sec) based on MAF
                if maf is not None and maf > 0:
                    fuel_ml_per_s = maf / FUEL_DENSITY_G_PER_ML
                    fuel_l_per_hr = (fuel_ml_per_s * 3600.0) / ML_PER_LITER
                    fuel_gal_per_hr = fuel_l_per_hr / LITERS_PER_GALLON
                    self.trip["fuel_gallons"] += fuel_gal_per_hr / 3600.0

                # Samples counter
                self.trip["samples"] += 1

                # Average speed based on running average of valid speed samples
                if speed is not None and speed > 0:
                    self.trip["avg_speed"] = (
                        (self.trip["avg_speed"] * (self.trip["samples"] - 1) + speed)
                        / self.trip["samples"]
                    )

                # Trip-based average MPG: total miles / total gallons
                if self.trip["fuel_gallons"] > 0 and self.trip["miles"] > 0:
                    self.trip["avg_mpg"] = self.trip["miles"] / self.trip["fuel_gallons"]

                # Save every 10 seconds
                if (datetime.now() - self.last_save_time).total_seconds() > 10:
                    save_trip(self.trip)
                    self.last_save_time = datetime.now()

            # -----------------------------
            # End trip persistence logic
            # -----------------------------

            print(
                f"RPM: {smooth['rpm']} | Coolant: {smooth['coolant']} °C | "
                f"Speed: {smooth['speed']} mph | IAT: {smooth['iat']} °C | "
                f"MAF: {smooth['maf']} g/s | Fuel: {smooth['fuel_level']} % | "
                f"MPG (inst): {smooth['mpg']} | Trip MPG: {self.trip['avg_mpg']}"
            )

            time.sleep(TELEMETRY_INTERVAL)


if __name__ == "__main__":
    telemetry = Telemetry()
    telemetry.telemetry_loop()
