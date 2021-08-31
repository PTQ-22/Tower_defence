import pygame
from .tower import Tower
from game.button import Button
from game.colors import ColorsRGB


class LaserTower(Tower):

    RANGE = 200
    DAMAGE = 0.05
    PRICE = 100
    buy_field_y = 610
    add_button = Button(1460, 700, 180, 20, ColorsRGB.GREEN, text=f"BUY ${PRICE}")

    def __init__(self, x, y):
        super().__init__(x, y)

    @staticmethod
    def draw(win, mid_x, mid_y, barrel_x, barrel_y, x, y, width, height):
        pygame.draw.line(win, ColorsRGB.BROWN, (x, y), (x + width, y + height), 15)
        pygame.draw.line(win, ColorsRGB.BROWN, (x, y + height), (x + width, y), 15)
        pygame.draw.circle(win, ColorsRGB.BLUE, (mid_x, mid_y), 22)
        pygame.draw.circle(win, ColorsRGB.BLACK, (mid_x, mid_y), 12)
        pygame.draw.circle(win, ColorsRGB.RED, (mid_x, mid_y), 3)

    def shoot_to_target(self, win, enemies):
        if self.target is not None:
            self.target.hp -= self.DAMAGE

            self.draw_laser(win)

            if self.target.hp <= 0 or self.get_distance_to_enemy(self.target.x, self.target.y) > self.RANGE:
                self.target = None

    def draw_laser(self, win):
        pygame.draw.line(win, ColorsRGB.ORANGE, (self.x_middle, self.y_middle),
                         (self.target.x + self.target.width / 2, self.target.y + self.target.height / 2), 7)
