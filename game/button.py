import pygame
from game.colors import ColorsRGB
pygame.init()


class Button:
    def __init__(self, x, y, width, height, color, text='', font_size=20, border=True, font_color=ColorsRGB.BLACK):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.font_size = font_size
        self.border_size = 5
        self.border = border
        self.is_active = True
        self.no_paths = False
        self.font_color = font_color

    def draw(self, win):
        if self.border:
            pygame.draw.rect(win, ColorsRGB.BLACK, (
                self.x - self.border_size, self.y - self.border_size, self.width + self.border_size * 2,
                self.height + self.border_size * 2), 0, 3)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0, 3)
        if self.text != '':
            font = pygame.font.Font('freesansbold.ttf', self.font_size)
            text = font.render(self.text, True, self.font_color)
            win.blit(text,
                     (self.x + (self.width / 2 - text.get_width() / 2),
                      self.y + (self.height / 2 - text.get_height() / 2)))

    def is_mouse(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False
