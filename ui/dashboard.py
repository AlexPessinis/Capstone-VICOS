# ui/dashboard.py
#
# VICOS Dashboard Screen 
# ---------------------------------------
# Hello! This screen includes:
# - Navigation bar
# - RPM bar (5700 max, redline at 5500)
# - Coolant + Intake temp boxes
# - Average MPG
# - Speed
# - MAF
# Plus some stylistic choices from me. 
# ui/dashboard.py

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.graphics import Color, Rectangle

from ui.components.rpm_bar import RPMBar
from ui.components.temp_box import TempBox
from ui.components.mpg_display import MPGDisplay
from ui.components.speed_display import SpeedDisplay
from ui.components.maf_display import MAFDisplay
from ui.components.nav_button import NavButton


class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Global background
        with self.canvas.before:
            Color(0.05, 0.05, 0.05, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_bg, size=self.update_bg)

        # Root layout
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # --- NAV BAR ---
        nav_bar = BoxLayout(size_hint_y=0.12, spacing=10)

        nav_bar.add_widget(NavButton(
            text="Dashboard",
            screen_name="dashboard",
            app_ref=App.get_running_app()
        ))

        nav_bar.add_widget(NavButton(
            text="Trip",
            screen_name="trip",
            app_ref=App.get_running_app()
        ))

        root.add_widget(nav_bar)

        # --- TOP BAR (MPG + MAF) ---
        top_bar = BoxLayout(size_hint_y=0.15, spacing=10)

        # Apply retro font to MPG + MAF displays
        self.mpg_display = MPGDisplay(font_name="fonts/segment.ttf")
        self.maf_display = MAFDisplay(font_name="fonts/segment.ttf")

        top_bar.add_widget(self.mpg_display)
        top_bar.add_widget(self.maf_display)

        root.add_widget(top_bar)

        # --- MIDDLE SECTION (RPM + Temps) ---
        middle = BoxLayout(size_hint_y=0.55, spacing=10)

        # RPM section
        rpm_section = BoxLayout(orientation="vertical", size_hint_x=0.3, spacing=10)

        self.rpm_bar = RPMBar(size_hint_y=0.8)

        # Retro RPM label
        self.rpm_label = Label(
            text="RPM: --",
            font_name="fonts/segment.ttf",
            font_size="32sp",
            color=(1, 1, 1, 1)
        )

        rpm_section.add_widget(self.rpm_bar)
        rpm_section.add_widget(self.rpm_label)

        # Temperature section
        temp_section = BoxLayout(orientation="vertical", size_hint_x=0.7, spacing=10)

        # Apply retro font to TempBox labels
        self.coolant_box = TempBox(label_text="Coolant", font_name="fonts/segment.ttf")
        self.iat_box = TempBox(label_text="Intake Air", font_name="fonts/segment.ttf")

        temp_section.add_widget(self.coolant_box)
        temp_section.add_widget(self.iat_box)

        middle.add_widget(rpm_section)
        middle.add_widget(temp_section)

        root.add_widget(middle)

        # --- BOTTOM BAR (Speed) ---
        bottom_bar = BoxLayout(size_hint_y=0.30)

        # Retro font for speed display
        self.speed_display = SpeedDisplay(font_name="fonts/segment.ttf")
        bottom_bar.add_widget(self.speed_display)

        root.add_widget(bottom_bar)

        self.add_widget(root)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def update(self, data):
        rpm = data.get("rpm")
        coolant = data.get("coolant")
        speed = data.get("speed")
        iat = data.get("iat")
        maf = data.get("maf")
        mpg = data.get("mpg")

        # RPM
        self.rpm_bar.update(rpm)
        self.rpm_label.text = f"RPM: {int(rpm)}" if rpm else "RPM: --"

        # Temps
        self.coolant_box.update(coolant)
        self.iat_box.update(iat)

        # Speed
        self.speed_display.update(speed)

        # MPG
        self.mpg_display.update(mpg)

        # MAF
        self.maf_display.update(maf)
