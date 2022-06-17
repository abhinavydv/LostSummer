from widgets.walker import Walker


class Kunai(Walker):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = "assets/images/NinjaAdventure/Right_Kunai.png"
        self.use_gravity = False

    def on_collide(self, other, col):
        if other.tag != "player" and other.tag != "collectible" and other.tag != "enemy_collider":
            if not other.is_static:
                self.parent.parent.legends["score"].score += other.score_gain
                other.get_blown()
            self.clean_up()

    def animate(self, levelscreen, dt):
        if self.relative_velocity[0] < 0:
            self.direction = "Left"
        self.image = f"assets/images/NinjaAdventure/{self.direction}_Kunai.png"
