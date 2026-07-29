# ui/components/speed_display.py

from kivy.uix.label import Label


class SpeedDisplay(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 48
        self.text = "Speed: -- mph"

    def update(self, speed):
        if speed is None:
            self.text = "Speed: -- mph"
        else:
            self.text = f"Speed: {int(speed)} mph"
