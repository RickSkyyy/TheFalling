from kivy.app import App
from kivy.graphics import Ellipse, Rectangle, Color
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import Clock, ObjectProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
import random
from kivy.uix.relativelayout import RelativeLayout

Builder.load_file('menu.kv')


# How to play the game: Click left and right to move along the 'x' axis to stop click button to move in the opposite
# direction once, to go faster just repeatedly click the direction you want to go BUT there's a catch the faster
# you are going the harder it is to stop so be carefull. you can teleport to the other side of the screen but only from
# the right side to the left side

# Objective: Dodge all incoming enemies until you reach the next level

class Sprite():
    def __init__(self, x, y, size, color, vx, vy):
        '''Set all values.'''

        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.vx = vx
        self.vy = vy
        self.rect = None
        # self.alive = True

    def create_rect(self):
        '''Execute it in `with canvas:` in `on_size()`.'''

        Color(*self.color)
        self.rect = Rectangle(pos=(self.x, self.y), size=(self.size, self.size))

    def set_start_pos(self, center_x, center_y):
        '''Move to start position.'''

        self.x = center_x + self.start_x
        self.y = center_y + self.start_y

    def move(self):
        '''Calculate new position without moving object on `canvas`.'''

        self.x += self.vx
        self.y += self.vy

    def draw(self):
        '''Move object on canvas.'''

        self.rect.pos = (self.x, self.y)

    def check_collision_circle(self, other):
        distance = (((self.x - other.x) ** 2) + ((self.y - other.y) ** 2)) ** 0.5

        # if distance < (self.size + other.size)/2:
        #    print(True)
        #    return True
        # else:
        #    return False

        return distance < (self.size + other.size) / 2

    def check_collision_rect(self, other):
        # code `... and ...` gives `True` or `False`
        # and it doesn't need `if ...: return True else: return False`

        return ((other.x <= self.x + self.size) and
                (self.x <= other.x + other.size) and
                (other.y <= self.y + self.size) and
                (self.y <= other.y + other.size))


class MainCanvas(Widget):
    rec_x = NumericProperty(0)
    inc = dp(3)
    ball_size = dp(35)
    my_player = ObjectProperty(Rectangle)

    count = 0
    score = StringProperty('0')
    score_inc = 1

    menu_widget = ObjectProperty()
    right_button = ObjectProperty()
    left_button = ObjectProperty()

    state_game_over = False
    state_game_has_started = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.player = Sprite(x=-self.ball_size / 2, y=145, size=dp(15), vx=dp(0), vy=dp(0), color=(1, .3, .5))

        self.balls = [
            Sprite(x=-15, y=-2000, size=dp(15), vx=dp(0), vy=dp(3), color=(1, 0, 0)),  # Red
            Sprite(x=100, y=-900, size=dp(15), vx=dp(0), vy=dp(5), color=(1, 1, 0)),  # Yellow
            Sprite(x=-300, y=-1000, size=dp(30), vx=dp(0), vy=dp(5), color=(1, 0, 1)),  # Purple
            Sprite(x=300, y=-600, size=dp(15), vx=dp(0), vy=dp(5), color=(1, 1, 1)),  # White
            Sprite(x=50, y=-3000, size=dp(17), vx=dp(0), vy=dp(7), color=(1, .5, 0)),  # Orange
            Sprite(x=100, y=-1200, size=dp(9), vx=dp(0), vy=dp(3), color=(1, .5, .7)),  # Pink
            Sprite(x=255, y=-1200, size=dp(9), vx=dp(0), vy=dp(3), color=(1, .5, .7)),  # Pink
            Sprite(x=-400, y=-1900, size=dp(30), vx=dp(0), vy=dp(5), color=(.5, 0, 1)),  # Dark Purple
            Sprite(x=350, y=-6000, size=dp(15), vx=dp(0), vy=dp(5), color=(.5, .5, .5)),  # Grey

            Sprite(x=15, y=-20000, size=dp(15), vx=dp(0), vy=dp(10), color=(1, 0, 0)),  # Red
            Sprite(x=170, y=-9000, size=dp(15), vx=dp(0), vy=dp(7), color=(1, 1, 0)),  # Yellow
            Sprite(x=-350, y=-10000, size=dp(30), vx=dp(0), vy=dp(7), color=(1, 0, 1)),  # Purple
            Sprite(x=320, y=-6000, size=dp(15), vx=dp(0), vy=dp(7), color=(1, 1, 1)),  # White
            Sprite(x=50, y=-30000, size=dp(17), vx=dp(0), vy=dp(8), color=(1, .5, 0)),  # Orange
            Sprite(x=110, y=-12000, size=dp(9), vx=dp(0), vy=dp(4), color=(1, .5, .7)),  # Pink
            Sprite(x=-420, y=-19000, size=dp(30), vx=dp(0), vy=dp(6), color=(.5, 0, 1)),  # Dark Purple
            Sprite(x=370, y=-60000, size=dp(15), vx=dp(0), vy=dp(7), color=(.5, .5, .5)),  # Grey

            Sprite(x=-40, y=-2500, size=dp(15), vx=dp(0), vy=dp(8), color=(1, 0, 0)),  # Red
            Sprite(x=175, y=-1500, size=dp(15), vx=dp(0), vy=dp(5), color=(1, 1, 0)),  # Yellow
            Sprite(x=-323, y=-1800, size=dp(30), vx=dp(0), vy=dp(5), color=(1, 0, 1)),  # Purple
            Sprite(x=360, y=-1000, size=dp(15), vx=dp(0), vy=dp(5), color=(1, 1, 1)),  # White
            Sprite(x=90, y=-3900, size=dp(17), vx=dp(0), vy=dp(7), color=(1, .5, 0)),  # Orange
            Sprite(x=240, y=-2500, size=dp(9), vx=dp(0), vy=dp(3), color=(1, .5, .7)),  # Pink
            Sprite(x=-200, y=-1900, size=dp(30), vx=dp(0), vy=dp(5), color=(.5, 0, 1)),  # Dark Purple
            Sprite(x=4500, y=-7900, size=dp(15), vx=dp(0), vy=dp(5), color=(.5, .5, .5)),  # Grey

            Sprite(x=0, y=-25000, size=dp(15), vx=dp(0), vy=dp(10), color=(1, 0, 0)),  # Red
            Sprite(x=170, y=-19000, size=dp(15), vx=dp(0), vy=dp(7), color=(1, 1, 0)),  # Yellow
            Sprite(x=-350, y=-15000, size=dp(30), vx=dp(0), vy=dp(7), color=(1, 0, 1)),  # Purple
            Sprite(x=-320, y=-6000, size=dp(15), vx=dp(0), vy=dp(7), color=(1, 1, 1)),  # White
            Sprite(x=100, y=-35000, size=dp(17), vx=dp(0), vy=dp(8), color=(1, .5, 0)),  # Orange
            Sprite(x=220, y=-12000, size=dp(9), vx=dp(0), vy=dp(4), color=(1, .5, .7)),  # Pink
            Sprite(x=-320, y=-12000, size=dp(30), vx=dp(0), vy=dp(6), color=(.5, 0, 1)),  # Dark Purple
            Sprite(x=270, y=-55000, size=dp(15), vx=dp(0), vy=dp(7), color=(.5, .5, .5)),  # Grey
        ]

        '''self.balls = [
            Sprite(x=0, y=-2000, size=dp(15), vx=dp(0), vy=dp(8), color=(1, 0, 0)),
            Sprite(x=100, y=-1000, size=dp(15), vx=dp(0), vy=dp(5), color=(1, 1, 0)),
            Sprite(x=-300, y=-1000, size=dp(30), vx=dp(0), vy=dp(5), color=(1, 0, 1)),
            Sprite(x=300, y=-600, size=dp(15), vx=dp(0), vy=dp(5), color=(1, 1, 1)),
        ]'''

        with self.canvas:
            for ball in self.balls:
                ball.create_rect()

            self.player.create_rect()

        Clock.schedule_interval(self.update, 1 / 60)
        Clock.schedule_interval(self.scorekeeper, self.score_inc)

    def scorekeeper(self, dt):
        if not self.state_game_over and self.state_game_has_started:
            self.score = str(self.count)
            self.count += 1

    def reset_game(self):
        self.state_game_over = False
        self.player.x = 382.5
        self.player.vx = 0
        self.count = 0

    def on_size(self, *args):
        print(f'on_size : {self.width}x{self.height}')

        for ball in self.balls:
            ball.set_start_pos(self.center_x, self.center_y)

        self.player.set_start_pos(self.center_x, self.center_y)

        self.rec_x = self.player.x

    def update(self, dt):

        # x = 382.5 y = 445.0

        # all in one function to control if it check collision after move, and draw only after all calculations

        # --- moves (without draws) ---

        self.player_move(dt)

        # move green rectangle below player
        self.rec_x = self.player.x + dp(7.5)

        self.ball_move(dt)

        # --- collisions (without draws) ---

        live_balls = []

        '''PLAYER BEING HIT'''

        for ball in self.balls:
            if self.player.check_collision_rect(ball) and not self.state_game_over:
                # if self.player.check_collision_circle(ball):
                print('killed')

                self.state_game_over = True
                self.menu_widget.opacity = 1
                # hide
                # ball.set_start_pos(self.center_x, self.center_y)
                # ball.draw()

                # or remove from canvas
                self.canvas.remove(ball.rect)
            else:
                live_balls.append(ball)

        self.balls = live_balls

        # --- draws ---

        self.player.draw()

        for ball in self.balls:
            ball.draw()

    def on_left_click(self):
        if not self.state_game_over and self.state_game_has_started:
            print('Left Clicked')
            self.player.vx -= self.inc

    def on_right_click(self):
        if not self.state_game_over and self.state_game_has_started:
            print('Right Clicked')
            self.player.vx += self.inc

    def ball_move(self, dt):
        for ball in self.balls:
            ball.move()

            if ball.y + ball.size > self.height:
                ball.set_start_pos(self.center_x, self.center_y)

    def player_move(self, dt):
        self.player.move()

        # moving left and stop on screen border
        if self.player.vx < 0 and self.player.x < 0:
            self.player.x = 0
            self.player.vx = 0

            # moving right and jump to left side when leave screen
        if self.player.vx > 0 and self.width < self.player.x:
            self.player.x = 0

    def on_menu_button_pressed(self):
        print('Button')
        self.reset_game()
        self.state_game_has_started = True
        self.menu_widget.opacity = 0
        self.left_button.opacity = .05
        self.right_button.opacity = .05


class TheFalling(App):
    pass


app = TheFalling()
app.run()
# app.stop()
app.root_window.close()


