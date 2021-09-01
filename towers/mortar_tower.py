import pygame
from .tower import Tower
from game.button import Button
from game.colors import ColorsRGB
from enemies.fly_enemy import FlyEnemy
import math


class MortarTower(Tower):

    RANGE = 500
    DAMAGE = 5
    PRICE = 300
    buy_field_y = 750
    add_button = Button(1460, 840, 180, 20, ColorsRGB.GREEN, text=f"BUY ${PRICE}")

    def __init__(self, x, y):
        super().__init__(x, y)
        self.flying_shells = []
        self.shot_counter = 400

    @staticmethod
    def draw(win, mid_x, mid_y, barrel_x, barrel_y, x, y, width, height):
        pygame.draw.circle(win, ColorsRGB.BLACK, (x + 10, y + 10), 10)
        pygame.draw.circle(win, ColorsRGB.BLACK, (x + width - 10, y + 10), 10)
        pygame.draw.circle(win, ColorsRGB.BLACK, (x + 10, y + height - 10), 10)
        pygame.draw.circle(win, ColorsRGB.BLACK, (x + width - 10, y + height - 10), 10)

        pygame.draw.circle(win, ColorsRGB.DARK_RED, (mid_x, mid_y), 22)
        pygame.draw.circle(win, ColorsRGB.BLACK, (mid_x, mid_y), 20)
        pygame.draw.circle(win, ColorsRGB.GREY, (mid_x, mid_y), 12)

    def shoot_to_target(self, win, enemies):
        if self.target is not None and type(self.target) != FlyEnemy:
            self.shot_counter += 1
            if self.shot_counter >= 500:
                self.shot_counter = 0
                self.flying_shells.append(Shell(self.x_middle, self.y_middle, self.target))

            if self.target.hp <= 0 or self.get_distance_to_enemy(self.target.x, self.target.y) > self.RANGE:
                self.target = None

        for shell in self.flying_shells:
            is_flying = shell.draw(win)
            if not is_flying:
                for enemy in enemies:
                    dist = math.sqrt((enemy.x - shell.x)**2 + (enemy.y - shell.y)**2)
                    if dist <= shell.RANGE:
                        enemy.hp -= self.DAMAGE
                self.flying_shells.remove(shell)


class Shell:

    FLY_SPEED = 0.006
    RANGE = 50

    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target_x = target.x
        self.target_y = target.y
        self.previous_dist_to_enemy = None
        self.new_dist_to_enemy = self.get_distance_to_enemy()
        self.x_dist = self.target_x - self.x
        self.y_dist = self.target_y - self.y
        self.x_fly_speed = self.FLY_SPEED * self.x_dist
        self.y_fly_speed = self.FLY_SPEED * self.y_dist

    def get_distance_to_enemy(self):
        return math.sqrt((self.target_x - self.x)**2 + (self.target_y - self.y)**2)

    def fly_to_targer(self):
        self.x += self.x_fly_speed
        self.y += self.y_fly_speed

        self.previous_dist_to_enemy = self.new_dist_to_enemy
        self.new_dist_to_enemy = self.get_distance_to_enemy()
        if self.new_dist_to_enemy > self.previous_dist_to_enemy:
            return False
        return True

    def draw(self, win):
        pygame.draw.circle(win, ColorsRGB.BLACK, (self.x, self.y), 10)
        is_flying = self.fly_to_targer()
        if is_flying:
            return True
        return False
