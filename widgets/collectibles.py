from widgets.walker import Walker
from widgets.sprite import DynamicSprite, StaticSprite
from widgets.jumper import Jumper
from widgets.periodic import Periodic


class Collectible(object):

    def __init__(self):
        super().__init__()
        self.max_relative_velocity = [.1, .4]
        self.tag = "collectible"

    def reveal(self, dt, block):
        # print("revealed")
        from kivy.clock import Clock
        self.interval = Clock.schedule_interval(
            lambda dt: self.go_up(dt, block), 0.01)

    def go_up(self, dt, block):
        # print("going up")
        # print(self.pos)
        self.relative_position[1] += self.max_relative_velocity[1] * dt
        # print(self.max_relative_velocity)
        # print(self.relative_position)
        if self.y > block.top:
            self.interval.cancel()
            if self.is_static:
                block.parent.parent.static_sprites.append(self)
            else:
                block.parent.parent.dynamic_sprites.append(self)


class Mushroom(Walker, Collectible):
    """
    The magical mushroom eating which makes mario bigger.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/images/items/Mushroom.png"
        self.tag = "powerup"

    def mario_collided(self, mario, col):
        mario.grow()
        self.clean_up()


class FireFlower(StaticSprite, Collectible):
    """
    The flower that gives mario the power to throw fireballs.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/images/items/Fire_Flower.png"
        self.tag = "powerup"

    def on_collide(self, other, col):
        if other.tag == "player":
            other.get_fire()
            self.clean_up()
        super().on_collide(other, col)


class PowerStar(Jumper, Collectible):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/images/items/StarPower.png"
        self.tag = "powerup"

    def mario_collided(self, mario, col):
        mario.be_invincible()
        self.clean_up()


class Coin(DynamicSprite, Collectible):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.images = ["assets/images/items/Coin_1.png",
                       "assets/images/items/Coin_2.png",
                       "assets/images/items/Coin_3.png",
                       "assets/images/items/Coin_4.png",
                       "assets/images/items/Coin_5.png",
                       "assets/images/items/Coin_6.png",
                       "assets/images/items/Coin_7.png",
                       "assets/images/items/Coin_8.png",
        ]
        self.i = 0
        self.collider = False

        from kivy.app import App
        self.gravity = App.get_running_app().settings["physics"]["gravity"]

    def reveal(self, dt, block):
        from kivy.clock import Clock
        self.interval = Clock.schedule_interval(self.go_up, 0.01)

    def go_up(self, dt):
        self.relative_position[1] += self.relative_velocity[1] * dt
        self.relative_velocity[1] += self.gravity * dt
        self.opacity -= self.relative_velocity[1] * dt

        self.image = self.images[self.i % 8]

        self.i += 1

        if self.relative_velocity[1] < -self.max_relative_velocity[1]/5:
            self.interval.cancel()

            self.parent.remove_widget(self)


class CollectibleHovering(Periodic):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag = "collectible"
        self.base_relative_position = [0, 0]
        self.hover_relative_height = 0.02

    def check_extreme(self, *args):
        if abs(self.relative_position[1] - self.base_relative_position[1]) > self.hover_relative_height:
            return True
        return False

    def on_extreme_reached(self, *args):
        self.relative_velocity[1] *= -1
        if self.relative_position[1] > self.base_relative_position[1]:
            self.relative_position[1] = self.base_relative_position[1] + self.hover_relative_height
        else:
            self.relative_position[1] = self.base_relative_position[1] - self.hover_relative_height
        self.relative_position[0] = self.base_relative_position[0]

    def on_collide(self, other, col):
        if other.tag == "player":
            self.player_collided(other, col)

    def player_collided(self, player, col):
        pass


class CollectibleKunai(CollectibleHovering):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/images/NinjaAdventure/Up_Kunai.png"

    def player_collided(self, player, col):
        player.get_kunai()
        self.clean_up()


class HealthPotion(CollectibleHovering):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/images/collectibles/Health_Potion.png"

    def player_collided(self, player, col):
        player.get_health_potion()
        self.clean_up()


class HoveringCoin(CollectibleHovering):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/images/items/Coin_1.png"
        self.i=1
        self.animation_time = 0

    def player_collided(self, player, col):
        player.get_coin()
        self.clean_up()

    def animate(self, levelscreen, dt):
        if self.i > 8:
            self.i = 1
        self.animation_time += dt

        if self.animation_time >= 0.1:
            self.i+=1
            self.animation_time = 0
        
        self.image = f"assets/images/items/Coin_{self.i}.png"


class SunKey(CollectibleHovering):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.image = "assets/images/collectibles/Key.png"

    def player_collided(self, player, col):
        player.get_sun_key()
        self.clean_up()