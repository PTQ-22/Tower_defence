import pygame
from game.colors import ColorsRGB
from game.button import Button
from levels.level_class import Level


class Menu:

    level_1_button = Button(650, 400, 400, 100, ColorsRGB.GREEN, text='START', font_size=40)

    @classmethod
    def draw(cls, win):
        win.fill(ColorsRGB.GREY)
        cls.level_1_button.draw(win)
        pos = pygame.mouse.get_pos()
        if cls.level_1_button.is_mouse(pos):
            cls.level_1_button.color = ColorsRGB.DARK_GREEN
        else:
            cls.level_1_button.color = ColorsRGB.GREEN

    @classmethod
    def draw_level(cls, win, current_level):
        if current_level == 0:
            cls.draw(win)
            current_level = cls.buttons_events()
        else:
            current_level.draw(win)
            current_level = current_level.buttons_events(win)

        return current_level

    @classmethod
    def buttons_events(cls):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if cls.level_1_button.is_mouse(pos):
                    return Level()

        return 0
