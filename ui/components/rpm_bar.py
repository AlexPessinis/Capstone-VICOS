# ui/components/rpm_bar.py

from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


class RPMBar(Widget):
    def __init__(self, max_rpm=5700, redline_start=5500, **kwargs):
        super().__init__(**kwargs)
        self.rpm = 0
        self.max_rpm = max_rpm
        self.redline_start = redline_start

    def update(self, rpm):
        self.rpm = rpm if rpm is not None else 0
        self.canvas.clear()

        fill_ratio = min(self.rpm / self.max_rpm, 1.0)
        fill_height = fill_ratio * self.height

        with self.canvas:
            # Background
            Color(0.05, 0.05, 0.05)
            Rectangle(pos=self.pos, size=self.size)

            # Determine color based on RPM
            if self.rpm < self.redline_start * 0.75:
                # Green zone
                Color(0.2, 0.8, 0.2)
            elif self.rpm < self.redline_start:
                # Yellow zone
                Color(0.9, 0.9, 0.2)
            else:
                # Red zone
                Color(0.9, 0.1, 0.1)

            Rectangle(pos=self.pos, size=(self.width, fill_height))
