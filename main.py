
# Set minimun window size
from kivy.config import Config
Config.set("graphics", "minimum_height", "200")
Config.set("graphics", "minimum_width", "200")
Config.set('graphics', 'window_state', 'maximized')

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window


# Window.clearcolor = (0, 0, 0, 1)


class LostSummerApp(MDApp):

    def build(self):
        """
        Bind the keyboard events so that keyboard works.
        Bind the size of the window to automatically resize the Game World.

        Apply the settings related to the game that depend on window size.
        """
        Window.bind(size=self.win_size_changed)
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)

        self.apply_settings(Window)

        from screens.homescreen import HomeScreen
        self.manager = ScreenManager(transition=NoTransition())
        self.manager.add_widget(HomeScreen())

        return self.manager

    def on_key_down(self, keyboard, ordinal, keycode, text, modifiers):
        """
        Listen to the key press events and pass them to the current screen.
        """
        self.manager.current_screen.on_key_down(
            keyboard, keycode, text, modifiers)

    def on_key_up(self, keyboard, _, keycode):
        """
        Listen to the key release events and pass them to the current screen.
        """
        self.manager.current_screen.on_key_up(keyboard, keycode)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_key_down)
        self._keyboard = None

    def apply_settings(self, Window):
        """
        Window: The window object of the current application.
        """
        from kivy.config import Config
        # don't close the app when escape is pressed
        Config.set("kivy", "exit_on_escape", 0)

        self.change_settings(Window)

    def win_size_changed(self, win_sdl, size):
        """
        win_sdl: The window SDL object.
        size: The new size of the Window.
        ___________________________________________________

        Gets executed when the size of the window changes.
        """
        self.change_settings(Window)
        self.manager.current_screen.win_size_changed(win_sdl, size)

        # if Window.width < Window.height/2:
        #     Window.size = (Window.size[1]/2, Window.size[1])
        # elif Window.height < Window.width/2:
        #     Window.height = Window.widht/2

    def change_settings(self, Window):
        """
        Window: The window object of the current application.
        _______________________________________________________

        Load the settings from the settings.json file.
        Then make changes to the settings and write to the file.
        """
        import json
        f = open("settings.json")
        self.settings = json.load(f)
        f.close()

        f = open("settings.json", "w")
        json.dump(self.settings, f)
        f.close()


if __name__ == "__main__":
    LostSummerApp().run()
