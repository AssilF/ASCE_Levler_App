from kivy.lang import Builder
from kivymd.app import MDApp

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette= "Crimson"
        return Builder.load_file("lvlrApp.kv")

    def on_start(self):
        super().on_start()

MainApp().run()
