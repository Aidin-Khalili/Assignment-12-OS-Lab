import arcade
from time import time 
from random import randint
import math

class spaceship(arcade.Sprite):
    def __init__(self, w):
        super().__init__(':resources:images/space_shooter/playerShip1_orange.png')
        self.width = 48
        self.height = 48
        self.speed = 5
        self.score = 0
        self.health = 5
        self.center_x = w // 2
        self.center_y = 48
        self.angle = 0
        self.change_angle = 0
        self.shot_list = []
    def rotating(self):
        self.angle += self.change_angle * self.speed
    def shotting(self):
        self.shot_list.append(Shot(self))
        
class Enemy(arcade.Sprite):
    def __init__(self, w, h, s = 2):
        super().__init__(':resources:images/space_shooter/playerShip1_blue.png')
        self.speed = s
        self.center_x = randint(0, w)
        self.center_y = h + h // 2
        self.angle = 180
        self.width = 48
        self.height = 48
    def hit_sound(self):
        arcade.play_sound(arcade.sound.Sound(':resources:sounds/hit1.wav'))
    def move(self):
        self.center_y -= self.speed

class Shot(arcade.Sprite):
    def __init__(self, host):
        super().__init__(':resources:images/space_shooter/laserRed01.png')
        self.angle = host.angle
        self.center_x = host.center_x
        self.center_y = host.center_y
        self.speed = 6
    def laser_sound(self):
        arcade.play_sound(arcade.sound.Sound(':resources:sounds/laser2.wav'), 0.2)
    def move(self):
        angle = math.radians(self.angle)
        self.center_x -= self.speed * math.sin(angle)
        self.center_y += self.speed * math.cos(angle)

class game(arcade.Window):
    def __init__(self):
        self.w = 800
        self.h = 600
        super().__init__(self.w, self.h, title = 'Star War')
        self.background_image = arcade.load_texture(':resources:images/backgrounds/stars.png')
        self.me = spaceship(self.w)
        self.enemy = Enemy(self.w, self.h)
        self.enemy_list = []
        self.next_enemy_time = randint(2, 5)
        self.game_start_time = time()
        self.start_time = time()
        self.health_image = arcade.load_texture('heart.png')
    def on_draw(self):
        arcade.start_render()
        if self.me.health <= 0:
            arcade.draw_text('Game over!', self.w // 2 - 200, self.h // 2, arcade.color.WHITE, 20, width = 400, align = 'center')
        else:
            arcade.draw_lrwh_rectangle_textured(0, 0, self.w, self.h, self.background_image)
            self.me.draw()
            for i in range(len(self.me.shot_list)):
                self.me.shot_list[i].draw()
            for i in range(len(self.enemy_list)):
                self.enemy_list[i].draw()
            for i in range(self.me.health):
                arcade.draw_lrwh_rectangle_textured(10 + i * 35, 10, 30, 30, self.health_image)
            arcade.draw_text('Score : ' + str(self.me.score), self.w - 130, 10, arcade.color.WHITE, 20, width = 200)
    def on_update(self, delta_time):
        self.end_time = time()
        if (self.end_time - self.start_time) > self.next_enemy_time:
            self.next_enemy_time = randint(4, 6)
            self.enemy_list.append(Enemy(self.w, self.h, int(3 + (self.end_time - self.game_start_time) // 24)))
            self.start_time = time()
        self.me.rotating()
        for i in range(len(self.me.shot_list)):
            self.me.shot_list[i].move()
        for i in range(len(self.enemy_list)):
            self.enemy_list[i].move()
        for enemy in self.enemy_list:
            for shot in self.me.shot_list:
                if arcade.check_for_collision(shot, enemy):
                    enemy.hit_sound()
                    self.me.shot_list.remove(shot)
                    self.enemy_list.remove(enemy)
                    self.me.score += 1
        for enemy in self.enemy_list:
            if enemy.center_y < 0:
                self.me.health -= 1
                self.enemy_list.remove(enemy)
        for shot in self.me.shot_list:
            if (shot.center_y > self.height) or (shot.center_x < 0) or (shot.center_x > self.width):
                self.me.shot_list.remove(shot)
    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.me.change_angle = 1
        elif key == arcade.key.RIGHT:
            self.me.change_angle = -1
        elif key == arcade.key.SPACE:
            self.me.shotting()
            self.me.shot_list[-1].laser_sound()
    def on_key_release(self, key, modifiers):
        self.me.change_angle = 0
            

my_game = game()
arcade.run()