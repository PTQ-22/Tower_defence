import pygame
from game.colors import ColorsRGB


class Enemy:

    def __init__(self, path):
        self.x = 40
        self.y = 460
        self.move_speed = 1

        self.hp = 10

        self.pos_in_grid = (6, 0)
        self.direction = 'right'
        self.path = path

        self.width = 10
        self.height = 30
        self.dist_to_new_square_x = 40
        self.dist_to_new_square_y = -10

    def draw(self, win):
        pygame.draw.rect(win, ColorsRGB.YELLOW, (self.x, self.y, self.width, self.height))
        pygame.draw.line(win, ColorsRGB.RED, (self.x - 10, self.y - 5), (self.x + self.width + 10, self.y - 5), 5)
        pygame.draw.line(win, ColorsRGB.GREEN, (self.x - 10, self.y - 5), (self.x + self.hp * 2, self.y - 5), 5)

    def move(self, grid):
        rect_mid = self.is_rect_mid(grid)
        if rect_mid:
            next_square = self.path[0]
            self.path.pop(0)
            if len(self.path) == 0:
                return False
            if self.direction == 'right':
                if next_square[0] > self.pos_in_grid[0]:
                    self.direction = 'down'
                elif next_square[0] < self.pos_in_grid[0]:
                    self.direction = 'up'
            else:
                if next_square[1] != self.pos_in_grid[1]:
                    self.direction = 'right'
            self.pos_in_grid = next_square

        if self.direction == 'right':
            self.x += self.move_speed
        elif self.direction == 'up':
            self.y -= self.move_speed
        elif self.direction == 'down':
            self.y += self.move_speed
        return True

    def is_rect_mid(self, grid):
        if self.direction == 'right':
            square_mid_x = grid.start_x + grid.square_size * (self.pos_in_grid[1]) + (grid.square_size // 2)
            if square_mid_x == self.x:
                return True
        else:
            square_mid_y = grid.start_y + grid.square_size * (self.pos_in_grid[0]) + (grid.square_size // 2)
            if square_mid_y == self.y:
                return True
        return False

    def draw_hit(self, win):
        pygame.draw.circle(win, ColorsRGB.BLACK, (self.x + self.width / 2, self.y + self.height / 2), 10)
        pygame.draw.circle(win, ColorsRGB.YELLOW, (self.x + self.width / 2, self.y + self.height / 2), 4)
        pygame.draw.circle(win, ColorsRGB.RED, (self.x + self.width / 2, self.y + self.height / 2), 2)

    @staticmethod
    def draw_and_move_enemies(win, enemies, grid):
        order = None
        for enemy in enemies:
            enemy.draw(win)
            is_enemy_moving = enemy.move(grid)
            if not is_enemy_moving or enemy.hp <= 0:
                enemies.remove(enemy)
                if enemy.hp <= 0:
                    order = 'destroyed'
                if not is_enemy_moving:
                    order = 'out'
        return enemies, order