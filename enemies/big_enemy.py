import pygame
from .enemy import Enemy


class BigEnemy(Enemy):

    MOVE_SPEED = 0.5
    START_HP = 200
    REWARD = 50
    IMAGES = [pygame.image.load(f"./images/big_enemy/big_enemy_{i+1}.png") for i in range(8)]

    def __init__(self, full_path):
        super().__init__(full_path)
        self.width = 65
        self.height = 50
        self.hp_bar_multiplier = 0.3
        self.x_and_y_back = 10
