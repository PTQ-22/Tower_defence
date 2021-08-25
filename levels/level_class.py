import pygame
from grid.grid import Grid
from game.colors import ColorsRGB
from game.button import Button
from towers.tower import Tower
from enemies.enemy import Enemy


class Level:
    grid = Grid()
    towers_to_buy = [
        Tower
    ]
    builded_towers = []
    enemies = []

    pygame.time.set_timer(pygame.USEREVENT, 1000)
    time_of_prepare_phase = 10
    counter = time_of_prepare_phase
    phase = 'prepare'

    money = 30
    lives = 5
    reward = 2

    @classmethod
    def draw(cls, win):
        win.fill(ColorsRGB.GREY)
        pygame.draw.rect(win, ColorsRGB.BROWN, (1430, 250, 240, 650), 0, 10)
        if cls.phase == "prepare":
            Button(1430, 40, 240, 20, ColorsRGB.GREY,
                   text=str(cls.counter), font_size=40, border=False, font_color=ColorsRGB.WHITE).draw(win)
        Button(1430, 100, 240, 20, ColorsRGB.GREY,
               text=f"Money: {cls.money}", font_size=30, border=False, font_color=ColorsRGB.YELLOW).draw(win)
        Button(1430, 150, 240, 20, ColorsRGB.GREY,
               text=f"Lives: {cls.lives}", font_size=20, border=False, font_color=ColorsRGB.RED).draw(win)

        Tower.draw_buttons(win)
        cls.grid.draw(win)

        if cls.phase == "battle":
            cls.enemies, order = Enemy.draw_and_move_enemies(win, cls.enemies, cls.grid)
            if len(cls.enemies) == 0:
                cls.phase = 'prepare'
            if order == 'destroyed':
                cls.money += cls.reward
            elif order == "out":
                cls.lives -= 1
            Tower.search_for_enemies(cls.builded_towers, cls.enemies)

        for tower in cls.builded_towers:
            tower.draw_on_grid(win, cls.grid.square_size+5)

    @classmethod
    def buttons_events(cls, win):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1

            if event.type == pygame.USEREVENT and cls.phase == "prepare":
                cls.start_battle_phase()
            if event.type == pygame.USEREVENT and cls.phase == "battle":  # TEST
                cls.enemies.append(Enemy(cls.grid.get_path()))

            if event.type == pygame.MOUSEBUTTONDOWN and cls.phase == 'prepare' and cls.money >= Tower.PRICE:
                cls.build_new_tower(win)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cls.enemies.append(Enemy(cls.grid.get_path()))

        return cls

    @classmethod
    def build_new_tower(cls, win):
        pos = pygame.mouse.get_pos()
        for tower in cls.towers_to_buy:
            if tower.add_button.is_mouse(pos):
                new_tower_position_items = tower.wait_for_find_place(cls.grid, cls, win)
                if new_tower_position_items:
                    rect_idx = new_tower_position_items[0]
                    old = cls.grid.array_2d[rect_idx[1]][rect_idx[0]]
                    cls.grid.array_2d[rect_idx[1]][rect_idx[0]] = 't'
                    if cls.grid.get_path():
                        cls.builded_towers.append(Tower(new_tower_position_items[1], new_tower_position_items[2]))
                        cls.money -= Tower.PRICE
                    else:
                        cls.grid.array_2d[rect_idx[1]][rect_idx[0]] = old

    @classmethod
    def start_battle_phase(cls):
        cls.counter -= 1
        if cls.counter == -1:
            cls.counter = cls.time_of_prepare_phase
            cls.phase = 'battle'
            cls.enemies.append(Enemy(cls.grid.get_path()))
