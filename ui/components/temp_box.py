# ui/components/temp_box.py

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class TempBox(BoxLayout):
    def __init__(self, label_text="Temp", **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        self.label = Label(text=label_text, font_size=24)
        self.value = Label(text="-- °C", font_size=32)

        self.add_widget(self.label)
        self.add_widget(self.value)

    def update(self, temp):
        if temp is None:
            self.value.text = "-- °C"
            self.value.color = (1, 1, 1, 1)
            return

        self.value.text = f"{temp:.1f} °C"

        # Color coding
        if temp < 70:
            self.value.color = (0.3, 0.8, 1, 1)  # cool
        elif temp < 95:
            self.value.color = (0.3, 1, 0.3, 1)  # normal
        else:
            self.value.color = (1, 0.2, 0.2, 1)  # hot
