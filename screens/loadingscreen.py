from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.lang import Builder


Builder.load_file("screens/loadingscreen.kv")


class LoadingScreen(Screen):
    bg_image = StringProperty("assets/images/tiles/BGMain.png")

    def on_enter(self, *args):
        self.manager.current = "LevelScreen"
        self.manager.remove_widget(self)

    def on_key_down(self, keyboard, keycode, text, modifiers):
        pass

    def on_key_up(self, keyboard, keycode):
        pass

    def win_size_changed(self, win_sdl, size):
        pass