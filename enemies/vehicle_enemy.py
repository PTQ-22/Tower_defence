import pygame
from .enemy import Enemy


class VehicleEnemy(Enemy):

    MOVE_SPEED = 3
    START_HP = 20
    REWARD = 10
    IMAGES = [pygame.image.load("./images/vehicle_enemy/vehicle_enemy.png") for _ in range(8)]

    def __init__(self, full_path):
        super().__init__(full_path)
        self.width = 40
        self.hp_bar_multiplier = 2
