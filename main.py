# main.py
# Alexander Pessinis Presents:
# _    ________________  _____
# | |  / /  _/ ____/ __ \/ ___/
# | | / // // /   / / / /\__ \ 
# | |/ // // /___/ /_/ /___/ / 
# |___/___/\____/\____//____/                
# VICOS UI Root Application
# -------------------------
# Handles:
# - Kivy initialization
# - ScreenManager setup
# - Dashboard + Trip screens
# - Telemetry update loop (currently set to 20 Hz, you may edit this in modules/telemetry.py)
#
# The UI receives smoothed telemetry data from the VICOS telemetry pipeline.

import time
import threading

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.clock import Clock

from modules.telemetry import Telemetry
from modules.smoothing import Smoother

# Import your UI screens (to be created next)
from ui.dashboard import DashboardScreen
from ui.trip_screen import TripScreen


class VICOSScreenManager(ScreenManager):
    pass


class VICOSApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Telemetry + smoothing pipeline
        self.telemetry = Telemetry()
        self.smoother = Smoother()

        # Shared data dictionary for UI
        self.shared_data = {
            "rpm": 0,
            "coolant": 0,
            "speed": 0,
            "iat": 0,
            "maf": 0,
            "fuel_level": 0,
            "mpg": 0,
        }

    def build(self):
        # Screen manager with fade transitions
        sm = VICOSScreenManager(transition=FadeTransition())

        # Add screens
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(TripScreen(name="trip"))

        # Start telemetry thread
        threading.Thread(target=self.telemetry_loop, daemon=True).start()

        # Schedule UI updates at 20 Hz
        Clock.schedule_interval(self.update_ui, 1/20)

        return sm

    def telemetry_loop(self):
        """
        Background thread that reads raw telemetry,
        smooths it, and stores it in shared_data.
        """
        while True:
            raw = self.telemetry.read_raw()
            smooth = self.smoother.smooth(raw)

            # Update shared data dictionary
            for key in self.shared_data:
                self.shared_data[key] = smooth.get(key, None)

            time.sleep(0.05)  # 20 Hz

    def update_ui(self, dt):
        """
        Called by Kivy's Clock at 20 Hz.
        Pushes shared_data into the active screen.
        """
        screen = self.root.current_screen

        if hasattr(screen, "update"):
            screen.update(self.shared_data)


if __name__ == "__main__":
    VICOSApp().run()
