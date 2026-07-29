# ui/components/mpg_display.py

from kivy.uix.label import Label


class MPGDisplay(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 32
        self.text = "Avg MPG: --"

    def update(self, mpg):
        if mpg is None:
            self.text = "Avg MPG: --"
        else:
            self.text = f"Avg MPG: {mpg:.1f}"
