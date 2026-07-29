# ui/components/maf_display.py

from kivy.uix.label import Label


class MAFDisplay(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 24
        self.text = "MAF: -- g/s"

    def update(self, maf):
        if maf is None:
            self.text = "MAF: -- g/s"
        else:
            self.text = f"MAF: {maf:.1f} g/s"
