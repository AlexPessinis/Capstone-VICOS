# ui/components/nav_button.py

from kivy.uix.button import Button

class NavButton(Button):
    def __init__(self, text, screen_name, app_ref=None, **kwargs):
        super().__init__(**kwargs)

        self.text = text
        self.screen_name = screen_name
        self.app_ref = app_ref

        self.font_size = 28
        self.size_hint = (0.5, 1)
        self.background_normal = ""
        self.background_color = (0.15, 0.15, 0.15, 1)
        self.color = (1, 1, 1, 1)

        self.bind(on_press=self.switch_screen)

    def switch_screen(self, instance):
        if self.app_ref:
            self.app_ref.root.current = self.screen_name
