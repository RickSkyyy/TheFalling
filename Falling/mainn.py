
from kivy.app import App
from kivy.graphics import Ellipse, Rectangle, Color
from kivy.metrics import dp
from kivy.properties import Clock, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget


# How to play the game: Click left and right to move along the 'x' axis to stop click button to move in the opposite
# direction once, to go faster just repeatedly click the direction you want to go BUT there's a catch the faster
# you are going the harder it is to stop sp be carefull. you can teleport to the other side of the screen but only from
# the right side to the left side

# Objective: Dodge all incoming enemies until you reach the next level

# Level layout: Lvl 1: Space invaders type mode Lvl 2: Platform runner type mode Lvl 3: undecided...

# Goal: Make this game playable both on mobile and pc


class MainCanvas(Widget):
    rec_x = Widget.center_x  # this helps the enemies know where you are
    rec_y = Widget.height
    inc = dp(3)
    ball_size = dp(35)
    right_button = ObjectProperty()
    my_player = ObjectProperty(Rectangle)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Object properties

        self.player_size = dp(15)
        self.ball_size = dp(15)
        self.ball2_size = dp(15)
        self.ball3_size = dp(30)
        self.ball4_size = dp(15)
        self.vx = dp(0)
        self.vy = dp(8)
        self.vy2 = dp(5)
        self.vy3 = dp(5)
        self.vy4 = dp(5)
        with self.canvas:
            Color(1, 0, 0)
            self.ball = Rectangle(pos=(self.center_x, self.center_y), size=(self.ball_size, self.ball_size))
            Color(1, 1, 0)
            self.ball2 = Rectangle(pos=(self.center_x, self.center_y), size=(self.ball2_size, self.ball2_size))
            Color(1, 1, 1)
            self.ball3 = Rectangle(pos=(self.center_x, self.center_y), size=(dp(30), dp(30)))
            self.ball4 = Rectangle(pos=(self.center_x, self.center_y), size=(self.ball2_size, self.ball2_size))
            Color(1, .3, .5)
            self.player = Rectangle(pos=(self.rec_x, self.rec_y), size=(self.player_size, self.player_size))
        Clock.schedule_interval(self.ball_movement, 1 / 60)
        #Clock.schedule_interval(self.distance_collides, 1 / 60)

    def on_size(self, *args):
        # print('on_size : ' + str(self.width) + ',' + str(self.height))
        self.ball.pos = (self.center_x - self.ball_size / 2, self.center_y - 1500)
        self.ball2.pos = (self.center_x + 200, self.center_y - 1000)
        self.ball3.pos = (self.center_x+400, self.center_y-1000)
        self.ball4.pos = (self.center_x + 500, self.center_y - 600)
        self.player.pos = (self.center_x-self.player_size / 2, self.center_y+145)

    def ball_movement(self, qt):

        x, y = self.ball.pos
        x2, y2 = self.ball2.pos
        x3, y3 = self.ball3.pos
        x4, y4 = self.ball4.pos

        x4 += self.vx
        y4 += self.vy4

        x3 += self.vx
        y3 += self.vy3

        x2 += self.vx
        y2 += self.vy2

        x += self.vx
        y += self.vy

        self.ball.pos = (x, y)
        self.ball2.pos = (x2, y2)
        self.ball3.pos = (x3, y3)
        self.ball4.pos = (x4, y4)

        # Enemy spawning algorithm, each enemy spawns at the center and the center of the world is where ever thr green
        # square is, the green square follows the character, and each enemy spawns at a different time giving the
        # illusion of random enemies spawning. Extra Info:After the enemy leaves the screen their position is reset
        # under the screen wherever the center is at that time. rec_x is the center.

        if y + self.ball_size > self.height + 400:
            self.ball.pos = int(self.center_x - self.ball_size / 2), int(self.center_y - 2000)

        if y2 + self.ball2_size > self.height + 40:
            self.ball2.pos = self.center_x - self.ball_size / 2, self.center_y - 700

        if y3 + self.ball3_size > self.height + 150:
            self.ball3.pos = self.center_x - self.ball_size / 2, self.center_y - 1100

        if y4 + self.ball4_size > self.height + 150:
            self.ball4.pos = self.center_x - self.ball_size / 2, self.center_y - 1100

        # print(self.player.size[0])

        # player_pos = (self.rec_x, self.rec_y)
        # print(player_pos)

        # if self.ball.pos < self.ball.pos:
            # print('YESSSSS')

        # print('POS:' + str(self.rec_x))
        # print('BOS:' + str(self.ball.pos))

    def on_left_click(self):
        print('Left Clicked')
        Clock.schedule_interval(self.left_movement, 1 / 60)

    def on_right_click(self):
        print('Right Clicked')
        Clock.schedule_interval(self.right_movement, 1 / 60)

    def left_movement(self, dt):
        xx, yy = self.player.pos
        player_x = xx
        player_y = yy
        self.player.pos = player_x - self.inc, player_y

        if int(player_x) < 0:
            self.player.pos = -1, player_y

        # After the enemies disappear they spawn under the green square the follows the main character this is usefull
        # so a player cant stay in the same place for long because the green square which will be invisible during
        # gameplay is telling the enemies where to spawn. extra explanation: rec_x acts as the center if the world.
        # the enemies pawn where ever the center is when by the time of their individual spawn.

        self.rec_x = self.rec_x - self.inc

        if self.rec_x < 0:
            self.rec_x = 13



    def right_movement(self, dt):
        xx, yy = self.player.pos
        player_x = xx
        player_y = yy
        self.player.pos = player_x + self.inc, player_y

        if self.width < int(player_x):
            self.player.pos = 0, player_y

        self.rec_x = self.rec_x + self.inc

        if self.width < self.rec_x:
            self.rec_x = -5




    #def distance_collides(player, ball):



        #distance = (((player.x-ball.x) ** 2) + ((player.y-ball.y) ** 2)) ** 0.5
        #if distance < (player.w + ball.w)/2.0:
            #return True
        #else:
            #return False

       # r1x = player.pos[0]
       # r1y = player.pos[1]
       # r2x = ball2.pos[0]
       # r2y = ball2.pos[1]
       # r1w = player.size[0]
      #  r1h = player.size[1]
      #  r2w = ball2.size[0]
       # r2h = ball2.size[1]

       # if r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y:
      #      print("True")
      #      return True
      #  else:
         #   return False
         #   print('False')


class TheFalling(App):
    pass


TheFalling().run()
