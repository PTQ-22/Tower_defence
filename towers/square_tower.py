import pygame
from .tower import Tower
from game.button import Button
from game.colors import ColorsRGB


class SquareTower(Tower):

    RANGE = 250
    DAMAGE = 10
    PRICE = 30
    buy_field_y = 470
    add_button = Button(1460, 560, 180, 20, ColorsRGB.GREEN, text=f"BUY ${PRICE}")

    SHOT_EVENT = pygame.USEREVENT + 3
    pygame.time.set_timer(SHOT_EVENT, 1200)

    def __init__(self, x, y):
        super().__init__(x, y)

    @staticmethod
    def draw(win, mid_x, mid_y, barrel_x, barrel_y, x, y, width, height):
        pygame.draw.rect(win, ColorsRGB.BROWN, (x, y, width, height))
        pygame.draw.line(win, ColorsRGB.BLACK, (mid_x, mid_y), (barrel_x, barrel_y), 20)
