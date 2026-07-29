# ui/components/reset_button.py

from kivy.uix.button import Button


class ResetButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "RESET TRIP"
        self.font_size = 48
        self.background_normal = ""
        self.background_color = (0.8, 0.1, 0.1, 1)
        self.size_hint = (0.75, 0.75)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
