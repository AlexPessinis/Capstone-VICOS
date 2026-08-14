from kivy.uix.button import Button
from kivy.properties import ListProperty

class ResetButton(Button):
    background_color = ListProperty([0.8, 0.1, 0.1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 120
        self.font_size = kwargs.get("font_size", 40)
        self.color = (1, 1, 1, 1)
        self.bold = True
