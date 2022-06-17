
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from widgets.legends import TextLabel

from widgets.walker import Walker
from time import time


class Ninja(Walker):
    """
    Definition of Player in the game.
    This class contains specifications of player.
    It contains methods that move him and detect collisions.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = "assets/images/NinjaAdventure/Right_Idle__001.png"
        self.relative_height = .1
        self.relative_width = .05

        self.tag = "player"
        self.max_relative_velocity = [.15, .4]

        self.standing = True
        self.is_invincible = False
        self.invincible_time = 0
        self.max_invincible_time = 20
        self.small = True
        self.has_fire = False
        self.min_time = 0.5
        self.fire_time = time()
        self.animate_time = time()

        self.direction = "Right"    # Right or Left
        self.state = "Idle"   # Run, Jump, Idle, Attack, Dead
        # self.dimension = "_Small"  # _Big or _Small (Size)
        self.power = ""  # <Blank string> or _Fire

        self.dying = False

        self.img_no = 0

        self._kunai_count = 10
        self.kunai_num_to_get = 10
        self.kunai_time = time()
        self.kunai_min_time = 0.5

        self._health = 3

        self.keyboard_disabled = False

        self.sounds = {}
        self.load_audio()

        # from kivy.core.audio import SoundLoader
        # sound = SoundLoader.load("assets/audio/sounds/bird.wav")

    def load_audio(self):
        l = [
        "assets/audio/GameAudio/BackgroundMusic.wav",
        "assets/audio/GameAudio/CollectCoin.wav",
        # "assets/audio/GameAudio/Decide.mp3",
        "assets/audio/GameAudio/EquipItem.wav",
        "assets/audio/GameAudio/FailureDrum.wav",
        # "assets/audio/GameAudio/GameStart.mp3",
        "assets/audio/GameAudio/Jump.wav",
        "assets/audio/GameAudio/KunaiThrow.wav",
        # "assets/audio/GameAudio/ShortSuccess.mp3",
        # "assets/audio/GameAudio/Success.mp3",
        "assets/audio/GameAudio/Sword.wav",
        "assets/audio/GameAudio/Win.wav",
        ]

        for i in l:
            self.sounds[i.split('/')[-1].split('.')[0]] = SoundLoader.load(i)
        # print(self.sounds)
        self.sounds["BackgroundMusic"].loop = True
        self.sounds["BackgroundMusic"].play()

    def play_sound(self, sound):
        # s=SoundLoader.load(self.sounds[sound])
        # s.on_stop = lambda *args: s.unload()
        # s.play()
        self.sounds[sound].seek(0)
        self.sounds[sound].volume = 0.5
        self.sounds[sound].play()

    @property
    def health(self):
        pass

    @health.setter
    def health(self, value):
        self.parent.parent.legends["lives"].count = value
        self._health = value

    @health.getter
    def health(self):
        return self._health

    @property
    def kunai_count(self):
        pass

    @kunai_count.setter
    def kunai_count(self, value):
        self.parent.parent.legends["kunai_count"].count = value
        self._kunai_count = value

    @kunai_count.getter
    def kunai_count(self):
        return self._kunai_count

    @property
    def score(self):
        pass

    @score.setter
    def score(self, value):
        self.parent.parent.legends["score"].score = value

    @score.getter
    def score(self):
        return self.parent.parent.legends["score"].score

    def get_added_to_screen(self, levelscreen):
        super().get_added_to_screen(levelscreen)

        levelscreen.player = self

    def on_collide(self, other, col):
        # if other.tag == "win":
        #     print("Won")
        #     self.win()
        if self.state == "Dead":
            return
        if other.tag == "powerup" or other.tag=="collectible" or other.tag == "enemy_collider":
            return
        if col[2] == "right":
            if not other.is_static:
                self.relative_velocity[0] = 0

        elif col[2] == "left":
            if not other.is_static:
                self.relative_velocity[0] = 0

        elif col[2] == "top":
            self.relative_velocity[1] = 0
            if self.jumping:
                self.jump2()
            elif self.state != "Run" and self.state != "Attack" and self.state != "Throw":
                self.state = "Idle"
                if self.relative_velocity[0] != 0:
                    self.state = "Run"

        elif col[2] == "bottom":
            self.relative_velocity[1] *= -1

        if other.is_static:
            other.move_aside(self, col)

    def win(self):
        lbl = TextLabel(text="You Win!", font_size=100, pos_hint={'x': 0.5, 'y': 0.5}, font_name="assets/fonts/Balloony.ttf", color=(0, 1, 0, 1))
        lbl.relative_font_size = 0.3
        lbl.keep_background = False
        self.parent.parent.bg_image = "assets/images/Tiles/SunnyBackground.png"
        self.parent.add_widget(lbl)
        self.parent.parent.win()

    def move(self, levelscreen, dt):
        # if self.position[0] > Window.height/2:
        # levelscreen.relative_screen_position[0] += (self.position[0]/Window.height - 0.5)
        # levelscreen.update_position()
        # self.relative_position[0] = self.relative_screen_position[0] + 0.5

        if self.state == "Dead":
            return

        if self.is_invincible:
            self.invincible_time += dt
            if self.invincible_time > self.max_invincible_time:
                self.is_invincible = False
                self.opacity = 1

        relative_half = Window.width / Window.height / 2
        if self.position[0] > Window.width/2: # and levelscreen.right_most_sprite.right > Window.width:
            levelscreen.relative_screen_position[0] += (
                self.position[0]-Window.width/2)/Window.height
            levelscreen.update_position()
            self.relative_position[0] = self.relative_screen_position[0] + relative_half

        if self.position[0] < Window.width/5:
            levelscreen.relative_screen_position[0] += (
                self.position[0]-Window.width/5)/Window.height
            levelscreen.update_position()
            self.relative_position[0] = self.relative_screen_position[0] + relative_half*2/5

        if self.position[1] > Window.height/2:
            levelscreen.relative_screen_position[1] += (self.position[1]/Window.height-0.5)
            levelscreen.update_position()
            self.relative_position[1] = self.relative_screen_position[1] + 0.5

        if self.position[1] < Window.height/4:
            levelscreen.relative_screen_position[1] += (self.position[1]/Window.height-0.25)
            levelscreen.update_position()
            self.relative_position[1] = self.relative_screen_position[1] + 0.25

        # if levelscreen.right_most_sprite.right < Window.width:
        #     levelscreen.relative_screen_position[0] -= (
        #         Window.width-levelscreen.right_most_sprite.right)/Window.height
        #     levelscreen.update_position()

        if self.relative_position[0] < self.relative_screen_position[0]:
            self.relative_position[0] = self.relative_screen_position[0]

        super().move(levelscreen, dt)

        if self.relative_position[1] < -1:
            self.die()

    def attack(self):
        self.img_no = 0
        if self.state == "Jump":
            self.state = "Jump_Attack"
        else:
            self.relative_velocity[0] = 0
            self.state = "Attack"
        self.keyboard_disabled = True

    def sit(self):
        self.relative_height = self.relative_width * 4/3
        self.state = "_Crouch"

    def stand(self):
        self.standing = True
        self.relative_height = self.relative_width * 2
        if self.state != "Jump":
            self.state = "Idle"

    def get_kunai(self):
        self.kunai_count += self.kunai_num_to_get
        self.play_sound("EquipItem")

    def get_health_potion(self, incr=1):
        self.health += incr

    def get_coin(self):
        self.score += 50
        self.play_sound("CollectCoin")

    def get_sun_key(self):
        self.score += 200
        self.win()

    def throw_kunai(self):
        if self.kunai_count:
            if time() - self.kunai_time > self.kunai_min_time:
                self.play_sound("KunaiThrow")
                self.img_no = 0
                if self.state == "Jump":
                    self.state = "Jump_Throw"
                else:
                    self.state = "Throw"
                self.kunai_count -= 1
                self.kunai_time = time()
                levelscreen = self.parent.parent
                content = levelscreen.sprites["Kunai"]
                content["name"] = "Kunai"
                content["relative_position"] = list(self.relative_position)
                content["relative_position"][0] += self.relative_width
                content["relative_position"][1] += self.relative_height/2
                content["relative_screen_position"] = self.relative_screen_position
                content["relative_velocity"][0] = content["max_relative_velocity"][0]
                if self.direction == "Left":
                    content["relative_position"][0] -= 2*self.relative_width
                    content["relative_velocity"][0] = - \
                        content["max_relative_velocity"][0]
                # return content
                levelscreen.add_one(content)

    def fireball(self):
        if self.has_fire:
            if time() - self.fire_time > self.min_time:
                self.fire_time = time()
                levelscreen = self.parent.parent
                content = levelscreen.sprites["FireBall"]
                content["name"] = "FireBall"
                content["relative_position"] = list(self.relative_position)
                content["relative_position"][0] += self.relative_width
                content["relative_position"][1] += self.relative_height
                content["relative_screen_position"] = self.relative_screen_position
                content["relative_velocity"][0] = content["max_relative_velocity"][0]

                if self.direction == "Left":
                    content["relative_position"][0] -= 2*self.relative_width
                    content["relative_velocity"][0] = - \
                        content["max_relative_velocity"][0]
                    content["direction"] = "Left"

                levelscreen.add_one(content)

    def jump2(self, multiplier=1):
        self.play_sound("Jump")
        self.state = "Jump"
        super().jump2(multiplier)

    def grow(self):
        if self.small:
            self.small = False
            self.dimension = "_Big"
            self.relative_height = 0.1
        else:
            self.get_fire()

    def be_invincible(self):
        self.is_invincible = True
        self.invincible_time = 0
        self.opacity = 0.5

    def get_fire(self):
        if self.small:
            self.grow()
        else:
            self.power = "_Fire"
            self.has_fire = True

    def on_key_down(self, keyboard, keycode, text, modifiers):
        if self.keyboard_disabled or self.parent.parent.paused:
            return

        if self.state == "Dead":
            return
        # print(self.state)
        if keycode == 79:  # Right Arrow key
            self.right_down()

        elif keycode == 80:  # Left Arrow key
            self.left_down()

        # elif keycode == 81:  # Down Arrow Key
        #     self.sit()

        # elif keycode == 82:  # Up Arrow Key
        #     if not self.standing:
        #         self.stand()

        elif keycode == 44:  # Space Bar
            self.space_down()

        elif keycode == 40:  # Enter Key
            self.enter_down()

        elif keycode == 20:   # Q
            self.attack()

    def right_down(self):
        self.relative_velocity[0] = self.max_relative_velocity[0]
        self.direction = "Right"
        if self.state != "Jump" and self.state != "Jump_Throw":
            self.state = "Run"

    def left_down(self):
        self.relative_velocity[0] = -self.max_relative_velocity[0]
        self.direction = "Left"
        if self.state != "Jump":
            self.state = "Run"

    def space_down(self):
        self.jumping = True

    def enter_down(self):
        self.throw_kunai()

    def on_key_up(self, keyboard, keycode):
        if self.keyboard_disabled:
            return

        if self.state == "Dead":
            return
        if keycode == 79:  # Right Arrow key
            self.right_up()

        if keycode == 80:  # Left Arrow key
            self.left_up()

        # if keycode == 81:   # Down Arrow key
        #     if self.state != "_Jump":
        #         self.state = "_Still"
        #         self.standing = True

        if keycode == 44:  # Space bar
            self.space_up()

    def right_up(self):
        self.relative_velocity[0] = 0
        if self.state != "Jump":
            self.state = "Idle"

    def left_up(self):
        self.right_up()

    def space_up(self):
        self.jumping = False

    def die(self):
        # if self.dying:
        #     print(self.state)
        #     self.parent.parent.end()
        self.health-=1
        self.kunai_count -= 5
        if self.kunai_count <= 0:
            self.kunai_count = 0
        if self.health <= 0:
            self.play_sound("FailureDrum")
            self.img_no = 0
            self.state = "Dead"
        else:
            self.invisible = True
            from kivy.clock import Clock
            self.blink_interval = Clock.schedule_interval(self.blink, 0.5)
            Clock.schedule_once(self.stop_blink, 5)
        # if self.small:
        #     # self.dying = True
        #     # self.jump2()
        #     # self.collider = False
        #     self.img_no = 0
        #     self.state = "Dead"
        #     # print(self.state)
        #     # print("d")

        # else:
        #     self.small = True
        #     self.has_fire = False
        #     self.power = ""
        #     self.relative_height = 0.06
        #     self.relative_width = 0.04
        #     self.dimension = "_Small"

        #     self.invisible = True

            # from kivy.clock import Clock
            # self.blink_interval = Clock.schedule_interval(self.blink, 0.5)
            # Clock.schedule_once(self.stop_blink, 5)

    def blink(self, dt):
        if self.opacity == 1:
            self.opacity = 0.5
        else:
            self.opacity = 1

    def stop_blink(self, dt):
        self.blink_interval.cancel()
        self.opacity = 1
        self.invisible = False

    def animate(self, levelscreen, dt):
        # if self.keyboard_disabled:
        #     print(self.state, self.img_no)

        images = 10
        interval = 0.05
        self.animate_time += dt
        if self.animate_time > interval:
            self.animate_time = 0
            self.img_no += 1
            if self.img_no >= images:
                if self.state == "Jump":
                    self.img_no = images-1
                elif self.state == "Dead":
                    self.img_no = images-1
                    self.parent.parent.end()
                elif self.state == "Attack" or self.state == "Throw":
                    self.keyboard_disabled = False
                    self.state = "Idle"
                    self.img_no = 0
                elif self.state == "Jump_Attack" or self.state == "Jump_Throw":
                    self.keyboard_disabled = False
                    self.state = "Jump"
                    self.img_no = 9
                else:
                    self.img_no = 0

        # if self.dying:
        image = f"assets/images/NinjaAdventure/{self.direction}_{self.state}__00{self.img_no}.png"
        # elif self.state == "_Walk":
        #     image = f"assets/images/mario/Mario{self.dimension}{self.direction}{self.state}_{self.img_no}{self.power}.png"
        # else:
        #     image = f"assets/images/mario/Mario{self.dimension}{self.direction}{self.state}{self.power}.png"

        # width, height = Image.open(image).size
        width, height = levelscreen.images[image]

        self.relative_width = self.relative_height * width / height
        self.image = image
