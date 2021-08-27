import pygame
from game.button import Button
from game.colors import ColorsRGB
from enemies.enemy import Enemy
import sys
import math


class Tower:

    add_button = Button(1460, 420, 180, 20, ColorsRGB.GREEN, text="BUY $10")
    RANGE = 150
    DAMAGE = 0.1 
    PRICE = 10 

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_middle = self.x + 37.5
        self.y_middle = self.y + 37.5
        self.barrel_x = self.x + 6
        self.barrel_y = self.y + 37.5
        self.barrel_move_val = 18.75
        self.target = None

    def draw_on_grid(self, win, rect_size):
        self.x_middle = self.x + 37.5
        self.y_middle = self.y + 37.5
        pygame.draw.circle(win, ColorsRGB.GREY, (self.x_middle, self.y_middle), rect_size / 4)
        pygame.draw.line(win, ColorsRGB.BLACK, (self.x_middle, self.y_middle),
                         (self.barrel_x, self.barrel_y), 10)
        if type(self.target) == Enemy:
            self.shoot_to_target(win)

    def shoot_to_target(self, win):
        self.target.hp -= self.DAMAGE

        self.move_barrel()

        self.target.draw_hit(win)
        pygame.draw.circle(win, ColorsRGB.YELLOW, (self.barrel_x, self.barrel_y), 6)
        pygame.draw.circle(win, ColorsRGB.RED, (self.barrel_x, self.barrel_y), 4)

        if self.target.hp <= 0:
            self.target = None

    def move_barrel(self):

        if self.target.x < self.x_middle - self.barrel_move_val:  # OK
            if self.target.y < self.y_middle - self.barrel_move_val:
                self.barrel_y = self.y + 15
                self.barrel_x = self.x + 15
            elif self.target.y > self.y_middle + self.barrel_move_val:
                self.barrel_y = self.y + 60
                self.barrel_x = self.x + 15
            else:
                self.barrel_y = self.y_middle
                self.barrel_x = self.x + 6
        elif self.target.x > self.x_middle + self.barrel_move_val:  # OK
            if self.target.y < self.y_middle - self.barrel_move_val:
                self.barrel_y = self.y + 15
                self.barrel_x = self.x + 60
            elif self.target.y > self.y_middle + self.barrel_move_val:
                self.barrel_y = self.y + 60
                self.barrel_x = self.x + 60
            else:
                self.barrel_y = self.y_middle
                self.barrel_x = self.x + 69
        else:  # OK
            if self.target.y < self.y_middle:
                self.barrel_y = self.y + 15
            elif self.target.y > self.y_middle:
                self.barrel_y = self.y + 60
            self.barrel_x = self.x_middle

    def get_distance_to_enemy(self, enemy_x, enemy_y):
        return math.sqrt((enemy_x - self.x)**2 + (enemy_y - self.y)**2)

    @classmethod
    def search_for_enemies(cls, towers, enemies):
        for tower in towers:
            if not tower.target or tower.get_distance_to_enemy(
                    tower.target.x + tower.target.width / 2,
                    tower.target.y + tower.target.height / 2) > cls.RANGE:
                for enemy in enemies:
                    dist_to_enemy = tower.get_distance_to_enemy(enemy.x, enemy.y)
                    if dist_to_enemy <= cls.RANGE:
                        tower.target = enemy

    @classmethod
    def draw_buttons(cls, win):
        pygame.draw.rect(win, ColorsRGB.WHITE, (1450, 330, 200, 130), 0, 20)
        pygame.draw.circle(win, ColorsRGB.GREY, (1550, 375), 18.75)
        pygame.draw.line(win, ColorsRGB.BLACK, (1550, 375),
                         (1513, 375), 10)
        cls.add_button.draw(win)
        if cls.add_button.is_active:
            pos = pygame.mouse.get_pos()
            if cls.add_button.is_mouse(pos):
                cls.add_button.color = ColorsRGB.DARK_GREEN
            else:
                cls.add_button.color = ColorsRGB.GREEN
        else:
            cls.add_button.color = ColorsRGB.GREY

    @classmethod
    def wait_for_find_place(cls, grid, level_copy, win):
        clock = pygame.time.Clock()
        transp_surface = pygame.Surface((1700, 915), pygame.SRCALPHA)
        while True:
            clock.tick(60)
            pos = pygame.mouse.get_pos()
            level_copy.draw(win)

            win.blit(transp_surface, (0, 0))
            pygame.draw.rect(transp_surface, (0, 0, 0, 0), (0, 0, 1700, 915))
            pygame.draw.circle(transp_surface, (0, 0, 250, 100), pos, Tower.RANGE, 150)

            pygame.draw.circle(win, ColorsRGB.GREY, pos, grid.rect_size / 4)
            pygame.draw.line(win, ColorsRGB.BLACK, pos,
                             (pos[0] - 31.5, pos[1]), 10)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.USEREVENT:
                    level_copy.counter -= 1
                if level_copy.counter <= 0:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    rect_index = cls.give_clicked_rect(pos, grid)
                    if rect_index and grid.array_2d[rect_index[1]][rect_index[0]] in [".", "p"]:
                        tower_x = rect_index[0] * grid.square_size
                        tower_y = rect_index[1] * grid.square_size
                        return [rect_index, tower_x, tower_y]

    @staticmethod
    def give_clicked_rect(pos, grid):
        for rect_y in range(grid.start_y, grid.start_y + grid.square_size * grid.height, grid.square_size):
            for rect_x in range(grid.start_x, grid.square_size * grid.width, grid.square_size):
                mouse_x, mouse_y = pos
                if rect_x < mouse_x < rect_x + grid.square_size:
                    if rect_y < mouse_y < rect_y + grid.square_size:
                        return rect_x // grid.square_size, rect_y // grid.square_size
        return False

