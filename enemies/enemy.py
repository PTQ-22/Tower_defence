import pygame
from game.colors import ColorsRGB


class Enemy:

    MOVE_SPEED = 1
    START_X = 40
    IMAGES = [pygame.image.load(f"./images/enemy/enemy_{i+1}.png") for i in range(8)]
    START_HP = 8
    REWARD = 5

    def __init__(self, full_path):
        self.x = self.START_X
        self.y = 460
        self.hp = self.START_HP
        self.hp_bar_multiplier = 1.5
        self.pos_in_grid = (6, 0)
        self.direction = "right"
        self.path = full_path
        self.width = 10
        self.height = 30
        self.animation_counter = 0
        self.x_and_y_back = 0

    def draw(self, win):
        self.draw_animated(win)
        self.draw_hp_bar(win)

    def draw_hp_bar(self, win):
        pygame.draw.line(win, ColorsRGB.RED, (self.x - 6 - self.x_and_y_back, self.y - 5 - self.x_and_y_back),
                         (self.x + self.START_HP * self.hp_bar_multiplier - self.x_and_y_back,
                          self.y - 5 - self.x_and_y_back), 5)
        pygame.draw.line(win, ColorsRGB.GREEN, (self.x - 6 - self.x_and_y_back, self.y - 5 - self.x_and_y_back),
                         (self.x + self.hp * self.hp_bar_multiplier - self.x_and_y_back,
                          self.y - 5 - self.x_and_y_back), 5)

    def draw_animated(self, win):
        self.animation_counter += 1
        if self.animation_counter >= 3 * len(self.IMAGES):
            self.animation_counter = 0
        win.blit(self.IMAGES[self.animation_counter // 3], (self.x - self.x_and_y_back, self.y - self.x_and_y_back))

    def move(self, grid):
        moving = self.change_direction(grid)
        if not moving:
            return False

        if self.direction == "right":
            self.x += self.MOVE_SPEED
        elif self.direction == "left":
            self.x -= self.MOVE_SPEED
        elif self.direction == "up":
            self.y -= self.MOVE_SPEED
        elif self.direction == "down":
            self.y += self.MOVE_SPEED

        return True

    def change_direction(self, grid):
        rect_mid = self.is_rect_mid(grid)
        if rect_mid:
            next_square = self.path[0]
            self.path.pop(0)
            if len(self.path) == 0:
                return False
            if self.direction == "right" or self.direction == "left":
                if next_square[0] > self.pos_in_grid[0]:
                    self.direction = "down"
                elif next_square[0] < self.pos_in_grid[0]:
                    self.direction = "up"
            else:
                if next_square[1] > self.pos_in_grid[1]:
                    self.direction = "right"
                elif next_square[1] < self.pos_in_grid[1]:
                    self.direction = "left"
            self.pos_in_grid = next_square
        return True

    def is_rect_mid(self, grid):
        if self.direction == "right":
            square_mid_x = grid.start_x + grid.square_size * (self.pos_in_grid[1]) + (grid.square_size // 2)
            if square_mid_x <= self.x + self.width / 2:
                return True
        if self.direction == "left":
            square_mid_x = grid.start_x + grid.square_size * (self.pos_in_grid[1]) + (grid.square_size // 2)
            if square_mid_x >= self.x + self.width / 2:
                return True
        elif self.direction == "up":
            square_mid_y = grid.start_y + grid.square_size * (self.pos_in_grid[0]) + (grid.square_size // 2)
            if square_mid_y >= self.y + self.height / 2:
                return True
        elif self.direction == "down":
            square_mid_y = grid.start_y + grid.square_size * (self.pos_in_grid[0]) + (grid.square_size // 2)
            if square_mid_y <= self.y + self.height / 2:
                return True
        return False

    def draw_hit(self, win):
        pygame.draw.circle(win, ColorsRGB.BLACK, (self.x + self.width / 2, self.y + self.height / 2), 10)
        pygame.draw.circle(win, ColorsRGB.YELLOW, (self.x + self.width / 2, self.y + self.height / 2), 4)
        pygame.draw.circle(win, ColorsRGB.RED, (self.x + self.width / 2, self.y + self.height / 2), 2)
