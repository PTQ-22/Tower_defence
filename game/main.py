import pygame
from game.menu import Menu


def main():
    win_size = (1700, 915)
    win = pygame.display.set_mode(win_size)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Tower Defence")

    current_level = 0
    framerate = 60
    loop = True
    while loop:
        clock.tick(framerate)

        current_level = Menu.draw_level(win, current_level)
        if current_level == -1:
            loop = False
        pygame.display.update()
