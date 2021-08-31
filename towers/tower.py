import pygame
from game.button import Button
from game.colors import ColorsRGB
import sys
import math


class Tower:

    RANGE = 150
    DAMAGE = 3
    PRICE = 10

    buy_field_y = 330
    add_button = Button(1460, 420, 180, 20, ColorsRGB.GREEN, text=f"BUY ${PRICE}")

    builded_towers = []

    SHOT_EVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(SHOT_EVENT, 500)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_middle = self.x + 37.5
        self.y_middle = self.y + 37.5
        self.barrel_x = self.x + 6
        self.barrel_y = self.y + 37.5
        self.barrel_move_val = 18.75
        self.target = None
        self.shot_animation_counter = 0
        self.animate_shot = False
        # self.clickable_area = Button(x, y, 75, 75, ColorsRGB.WHITE)
        # self.upgrade_button = Button(self.x_middle + 10, self.y_middle + 10, 25, 25, ColorsRGB.GREEN, border=False)
        # self.delete_button = Button(x + 10, self.y_middle + 10, 25, 25, ColorsRGB.RED, border=False)

    @staticmethod  # this method has unused arguments because can be override and other towers may need ex. x, y
    def draw(win, mid_x, mid_y, barrel_x, barrel_y, x, y, width, height):
        pygame.draw.circle(win, ColorsRGB.GREY, (mid_x, mid_y), 18.75)
        pygame.draw.line(win, ColorsRGB.BLACK, (mid_x, mid_y), (barrel_x, barrel_y), 10)

    def draw_on_grid(self, win, enemies):
        self.draw(win, self.x_middle, self.y_middle, self.barrel_x, self.barrel_y,
                  self.x + 13, self.y + 13, 50, 50)
        self.shoot_to_target(win, enemies)
        # pos = pygame.mouse.get_pos()
        # if self.clickable_area.is_mouse(pos):
        #     self.upgrade_button.draw(win)
        #     self.delete_button.draw(win)

    def shoot_to_target(self, win, enemies):
        if self.target is not None:
            self.move_barrel()
            if pygame.event.get(self.SHOT_EVENT):
                self.target.hp -= self.DAMAGE
                self.animate_shot = True
            if self.animate_shot:
                self.shot_animation_counter += 1
                if self.shot_animation_counter < 40:
                    self.draw_shot(win)
                    self.target.draw_hit(win)
                else:
                    self.animate_shot = False
                    self.shot_animation_counter = 0

            if self.target.hp <= 0 or self.get_distance_to_enemy(self.target.x, self.target.y) > self.RANGE:
                self.target = None

    def draw_shot(self, win):
        pygame.draw.circle(win, ColorsRGB.YELLOW, (self.barrel_x, self.barrel_y), 6)
        pygame.draw.circle(win, ColorsRGB.RED, (self.barrel_x, self.barrel_y), 4)

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

    def search_for_enemies(self, enemies):
        if not self.target or self.get_distance_to_enemy(
                self.target.x + self.target.width / 2,
                self.target.y + self.target.height / 2) > self.RANGE:
            for enemy in enemies:
                dist_to_enemy = self.get_distance_to_enemy(enemy.x, enemy.y)
                if dist_to_enemy <= self.RANGE:
                    self.target = enemy

    @classmethod
    def draw_buttons(cls, win):
        pygame.draw.rect(win, ColorsRGB.WHITE, (1450, cls.buy_field_y, 200, 130), 0, 20)
        cls.draw(win, 1550, cls.buy_field_y + 45, 1513, cls.buy_field_y + 45, 1525, cls.buy_field_y + 20, 50, 50)
        cls.add_button.draw(win)
        cls.change_buttons_colors()

    @classmethod
    def change_buttons_colors(cls):
        if cls.add_button.is_active:
            pos = pygame.mouse.get_pos()
            if cls.add_button.is_mouse(pos):
                cls.add_button.color = ColorsRGB.DARK_GREEN
            else:
                cls.add_button.color = ColorsRGB.GREEN
        else:
            cls.add_button.color = ColorsRGB.LIGHT_GREY

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
            pygame.draw.circle(transp_surface, (0, 0, 250, 100), pos, cls.RANGE, 1000)

            cls.draw(win, pos[0], pos[1], pos[0] - 31.5, pos[1], pos[0] - 25, pos[1] - 25, 50, 50)
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
