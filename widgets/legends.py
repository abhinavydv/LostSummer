from ast import Num
from kivy.properties import ListProperty, NumericProperty, StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window


Builder.load_file("widgets/legends.kv")


class Legend(Widget):

    relative_position = ListProperty([0, 0])
    relative_height = NumericProperty(0)
    relative_width = NumericProperty(0)
    keep_background = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.tag = "legend"

    def get_added_to_screen(self, levelscreen):
        self.pos_hint = {
            'x': self.relative_position[0], "y": self.relative_position[1]}
        self.size_hint = [self.relative_width, self.relative_height]
        levelscreen.legendlayout.add_widget(self)

    def update(self, levelscreen, dt):
        pass

    def set_attributes(self, data):
        for i in data:
            if isinstance(data[i], list):
                setattr(self, i, list(data[i]))
            elif isinstance(data[i], dict):
                setattr(self, i, dict(data[i]))
            else:
                setattr(self, i, data[i])


class TextLabel(Label, Legend):
    relative_font_size = NumericProperty(0.01)


class Score(Legend):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._score = 0
        self.lbl = None

    @property
    def score(self):
        pass

    @score.setter
    def score(self, value):
        self.lbl.text = "score: " + str(value)
        self._score = value

    @score.getter
    def score(self):
        return self._score

    def get_added_to_screen(self, levelscreen):
        self.lbl = TextLabel(text=f"Score: {self._score}")
        self.lbl.relative_font_size = self.relative_height/3
        self.add_widget(self.lbl)
        return super().get_added_to_screen(levelscreen)

    # def on_touch_down(self, touch):
    #     print(self.pos)
    #     print(self.size)
    #     print(Window.size)
    #     return super().on_touch_down(touch)


class Health(Legend):
    heart_image = StringProperty("")
    _count = NumericProperty(3)
    heart1 = ObjectProperty(None)
    heart2 = ObjectProperty(None)
    heart3 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.heart_image = "assets/images/collectibles/Heart.png"
        self.keep_background = False

    @property
    def count(self):
        pass

    @count.setter
    def count(self, value):
        # self.lbl.text = str(value)
        if value == 2:
            self.heart3.opacity = 0
        elif value == 1:
            self.heart2.opacity = 0
        else:
            self.heart1.opacity = 0
        self._count = value

    @count.getter
    def count(self):
        return self._count

    # def get_added_to_screen(self, levelscreen):
    #     # self.lbl = TextLabel(text=f"{self._count}")
    #     # self.add_widget(self.lbl)
    #     return super().get_added_to_screen(levelscreen)


class KunaiCount(Legend):
    kunai_image = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._count = 10
        self.kunai_image = "assets/images/NinjaAdventure/Up_Kunai.png"

    @property
    def count(self):
        pass

    @count.setter
    def count(self, value):
        self.lbl.text = str(value)
        self._count = value

    @count.getter
    def count(self):
        return self._count

    def get_added_to_screen(self, levelscreen):
        self.lbl = TextLabel(text=f"{self._count}")
        self.lbl.relative_font_size = self.relative_height/2
        self.add_widget(self.lbl)
        return super().get_added_to_screen(levelscreen)
