# ui/trip_screen.py
#
# VICOS Trip Summary Screen

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
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

        # Root layout (FloatLayout so we can place exit button)
        root = FloatLayout()

        # --- EMERGENCY EXIT BUTTON ---
        exit_button = Button(
            text="X",
            font_size="20sp",
            size_hint=(None, None),
            size=(40, 40),
            pos_hint={"right": 1, "top": 1},
            background_color=(1, 0, 0, 1),
            on_release=lambda *args: App.get_running_app().stop()
        )
        root.add_widget(exit_button)

        # --- MAIN VERTICAL STACK ---
        main_stack = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10,
            size_hint=(1, 1)
        )

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

        main_stack.add_widget(nav_bar)

        # --- TOP SECTION (Titles above values) ---
        top_section = BoxLayout(size_hint_y=0.35, spacing=20, padding=10)

        # Trip Miles
        trip_box = BoxLayout(orientation="vertical")
        trip_box.add_widget(Label(text="Trip Miles",
                                  font_size="32sp", color=(1, 1, 1, 1)))
        self.trip_miles_label = Label(text="--",
                                      font_size="48sp", color=(1, 1, 1, 1))
        trip_box.add_widget(self.trip_miles_label)

        # Avg Speed
        avg_box = BoxLayout(orientation="vertical")
        avg_box.add_widget(Label(text="Avg Speed",
                                 font_size="32sp", color=(1, 1, 1, 1)))
        self.avg_speed_label = Label(text="-- mph",
                                     font_size="48sp", color=(1, 1, 1, 1))
        avg_box.add_widget(self.avg_speed_label)

        # Top Speed
        top_box = BoxLayout(orientation="vertical")
        top_box.add_widget(Label(text="Top Speed",
                                 font_size="32sp", color=(1, 1, 1, 1)))
        self.top_speed_label = Label(text="-- mph",
                                     font_size="48sp", color=(1, 1, 1, 1))
        top_box.add_widget(self.top_speed_label)

        top_section.add_widget(trip_box)
        top_section.add_widget(avg_box)
        top_section.add_widget(top_box)

        main_stack.add_widget(top_section)

        # --- MIDDLE SECTION (Avg MPG) ---
        middle_section = BoxLayout(size_hint_y=0.25)
        self.avg_mpg_label = Label(text="Avg MPG: --",
                                   font_size="48sp", color=(1, 1, 1, 1))
        middle_section.add_widget(self.avg_mpg_label)
        main_stack.add_widget(middle_section)

        # --- BOTTOM SECTION (Reset Button) ---
        bottom_section = BoxLayout(size_hint_y=0.28)
        self.reset_button = ResetButton()
        self.reset_button.bind(on_press=self.reset_trip)
        bottom_section.add_widget(self.reset_button)
        main_stack.add_widget(bottom_section)

        # Add main stack to root
        root.add_widget(main_stack)
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

        # Trip calculations
        if speed is not None:
            self.trip_miles += (speed * 0.05) / 3600.0
            self.avg_speed = (self.avg_speed * 0.99) + (speed * 0.01)
            if speed > self.top_speed:
                self.top_speed = speed

        if mpg is not None:
            self.avg_mpg = (self.avg_mpg * 0.99) + (mpg * 0.01)

        # Update labels
        self.trip_miles_label.text = f"{self.trip_miles:.2f}"
        self.avg_speed_label.text = f"{self.avg_speed:.1f} mph"
        self.top_speed_label.text = f"{self.top_speed:.1f} mph"
        self.avg_mpg_label.text = f"Avg MPG: {self.avg_mpg:.1f}"

    def reset_trip(self, instance):
        self.trip_miles = 0
        self.avg_speed = 0
        self.top_speed = 0
        self.avg_mpg = 0

        self.trip_miles_label.text = "0.00"
        self.avg_speed_label.text = "0.0 mph"
        self.top_speed_label.text = "0.0 mph"
        self.avg_mpg_label.text = "Avg MPG: 0.0"
