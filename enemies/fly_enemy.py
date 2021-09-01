import pygame
from .enemy import Enemy


class FlyEnemy(Enemy):

    MOVE_SPEED = 2
    START_X = 40
    IMAGES = [pygame.image.load(f"./images/fly_enemy/fly_enemy_{i+1}.png") for i in range(8)]
    START_HP = 25
    REWARD = 20

    def __init__(self, full_path):
        super().__init__(full_path)
        self.width = 40
        self.height = 20
        self.hp_bar_multiplier = 1.8
        self.x_and_y_back = 15

    def change_direction(self, grid):
        if self.x >= 1330:
            return False
        return True
