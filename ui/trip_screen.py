# ui/trip_screen.py
#
# VICOS Trip Summary Screen
# -------------------------------------------
# Hello! This screen includes:
# - Navigation bar
# - Trip miles
# - Average speed
# - Top speed
# - Average MPG
# - Large reset button
# Plus some stylistic choices from me. 

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.graphics import Color, Rectangle

from ui.components.reset_button import ResetButton
from ui.components.nav_button import NavButton


class TripScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Background
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

        # --- TOP SECTION ---
        top_section = BoxLayout(size_hint_y=0.25, spacing=10)

        self.trip_miles_label = Label(text="Trip Miles: --", font_size=32, color=(1, 1, 1, 1))
        self.avg_speed_label = Label(text="Avg Speed: -- mph", font_size=32, color=(1, 1, 1, 1))
        self.top_speed_label = Label(text="Top Speed: -- mph", font_size=32, color=(1, 1, 1, 1))

        top_section.add_widget(self.trip_miles_label)
        top_section.add_widget(self.avg_speed_label)
        top_section.add_widget(self.top_speed_label)

        root.add_widget(top_section)

        # --- MIDDLE SECTION ---
        middle_section = BoxLayout(size_hint_y=0.35)

        self.avg_mpg_label = Label(text="Avg MPG: --", font_size=48, color=(1, 1, 1, 1))
        middle_section.add_widget(self.avg_mpg_label)

        root.add_widget(middle_section)

        # --- BOTTOM SECTION (Reset Button) ---
        bottom_section = BoxLayout(size_hint_y=0.25, padding=20)



        # Large red reset button
        self.reset_button = ResetButton(
            text="RESET TRIP",
            font_size=40,
            background_color=(0.8, 0.1, 0.1, 1)  # red
        )
        self.reset_button.bind(on_press=self.reset_trip)
        self.reset_button.size_hint = (1, None)
        self.reset_button.height = 120
        print("Reset button added:", self.reset_button)



        bottom_section.add_widget(self.reset_button)
        root.add_widget(bottom_section)

        self.add_widget(root)

        # Internal trip stats
        self.trip_miles = 0
        self.avg_speed = 0
        self.top_speed = 0
        self.avg_mpg = 0

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def update(self, data):
        speed = data.get("speed")
        mpg = data.get("mpg")

        # Trip stuff
        if speed is not None:
            self.trip_miles += (speed * 0.05) / 3600.0

        if speed is not None:
            self.avg_speed = (self.avg_speed * 0.99) + (speed * 0.01)

        if speed is not None and speed > self.top_speed:
            self.top_speed = speed

        if mpg is not None:
            self.avg_mpg = (self.avg_mpg * 0.99) + (mpg * 0.01)

        # Update labels
        self.trip_miles_label.text = f"Trip Miles: {self.trip_miles:.2f}"
        self.avg_speed_label.text = f"Avg Speed: {self.avg_speed:.1f} mph"
        self.top_speed_label.text = f"Top Speed: {self.top_speed:.1f} mph"
        self.avg_mpg_label.text = f"Avg MPG: {self.avg_mpg:.1f}"

    def reset_trip(self, instance):
        self.trip_miles = 0
        self.avg_speed = 0
        self.top_speed = 0
        self.avg_mpg = 0

        self.trip_miles_label.text = "Trip Miles: 0.00"
        self.avg_speed_label.text = "Avg Speed: 0.0 mph"
        self.top_speed_label.text = "Top Speed: 0.0 mph"
        self.avg_mpg_label.text = "Avg MPG: 0.0"
