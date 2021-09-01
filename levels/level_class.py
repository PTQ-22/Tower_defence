import pygame
from grid.grid import Grid
from game.colors import ColorsRGB
from game.button import Button
from towers.tower import Tower
from towers.square_tower import SquareTower
from towers.laser_tower import LaserTower
from towers.mortar_tower import MortarTower
from enemies.waves import waves_of_enemies


class Level:
    grid = Grid()
    skip_button = Button(1630, 65, 60, 30, ColorsRGB.WHITE, text="skip", font_size=20)
    towers_to_buy = [
        Tower,
        SquareTower,
        LaserTower,
        MortarTower
    ]

    enemies = []
    enemies_to_spawn = []

    SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1

    pygame.time.set_timer(pygame.USEREVENT, 1000)  # One second
    time_of_prepare_phase = 20
    counter = time_of_prepare_phase
    phase = "prepare"

    money = 300
    lives = 20
    wave_num = 0

    @classmethod
    def draw(cls, win):
        win.fill(ColorsRGB.GREY)
        pygame.draw.rect(win, ColorsRGB.BROWN, (1430, 250, 240, 650), 0, 10)

        cls.grid.draw(win)

        cls.draw_buttons(win)

        for tower_class in cls.towers_to_buy:
            tower_class.draw_buttons(win)
            for tower in tower_class.builded_towers:
                tower.draw_on_grid(win, cls.enemies)
                if cls.phase == "battle":
                    tower.search_for_enemies(cls.enemies)

        if cls.phase == "battle":
            cls.spawn_enemies()
            order = cls.draw_and_move_enemies(win)
            if len(cls.enemies) == 0 and len(cls.enemies_to_spawn) == 0:
                cls.phase = "prepare"
                if cls.wave_num >= len(waves_of_enemies):
                    cls.phase = "won"
            if order == "out":
                cls.lives -= 1
                if cls.lives <= 0:
                    cls.phase = "lost"

    @classmethod
    def draw_buttons(cls, win):
        Button(1430, 200, 240, 20, ColorsRGB.GREY, text=f"Money: {cls.money}", font_size=30, border=False,
               font_color=ColorsRGB.YELLOW).draw(win)
        Button(1430, 250, 240, 20, ColorsRGB.GREY, text=f"Allowed Escapes: {cls.lives}", font_size=20, border=False,
               font_color=ColorsRGB.RED).draw(win)
        if cls.phase == "prepare":
            Button(1400, 70, 240, 20, ColorsRGB.GREY, text=f"Time to battle: {cls.counter}", font_size=24, border=False,
                   font_color=ColorsRGB.WHITE).draw(win)
            Button(1430, 40, 240, 20, ColorsRGB.GREY, text=f"WAVE: {cls.wave_num + 1}", font_size=33, border=False,
                   font_color=ColorsRGB.GREEN).draw(win)
            cls.skip_button.draw(win)
        elif cls.phase == "battle":
            Button(1430, 40, 240, 20, ColorsRGB.GREY, text=f"WAVE: {cls.wave_num}", font_size=33, border=False,
                   font_color=ColorsRGB.GREEN).draw(win)
            Button(1430, 140, 240, 20, ColorsRGB.GREY, text=f"Living enemies: {len(cls.enemies)}", font_size=25,
                   border=False, font_color=ColorsRGB.DARK_RED).draw(win)
        elif cls.phase == "won":
            Button(720, 440, 0, 0, ColorsRGB.YELLOW, text="YOU WON", font_size=100, border=False,
                   font_color=ColorsRGB.GREEN).draw(win)
        elif cls.phase == "lost":
            Button(720, 440, 0, 0, ColorsRGB.YELLOW, text="YOU LOST", font_size=100, border=False,
                   font_color=ColorsRGB.RED).draw(win)

    @classmethod
    def draw_and_move_enemies(cls, win):
        order = None
        for enemy in cls.enemies:
            enemy.draw(win)
            is_enemy_moving = enemy.move(cls.grid)
            if not is_enemy_moving or enemy.hp <= 0:
                cls.enemies.remove(enemy)
                if enemy.hp <= 0:
                    order = "destroyed"
                    cls.money += enemy.REWARD
                if not is_enemy_moving:
                    order = "out"
        return order

    @classmethod
    def buttons_events(cls, win):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1

            pos = pygame.mouse.get_pos()
            if cls.skip_button.is_mouse(pos):
                cls.skip_button.color = ColorsRGB.ALMOST_WHITE
                if event.type == pygame.MOUSEBUTTONDOWN:
                    cls.counter = 0
            else:
                cls.skip_button.color = ColorsRGB.WHITE

            if event.type == pygame.USEREVENT and cls.phase == "prepare":
                cls.start_battle_phase()
            for tower_class in cls.towers_to_buy:
                if cls.phase == "prepare" and cls.money - tower_class.PRICE >= 0:
                    tower_class.add_button.is_active = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        cls.build_new_tower(win, tower_class)
                else:
                    tower_class.add_button.is_active = False

        return cls

    @classmethod
    def build_new_tower(cls, win, tower_class):
        pos = pygame.mouse.get_pos()
        if tower_class.add_button.is_mouse(pos):
            new_tower_position_items = tower_class.wait_for_find_place(cls.grid, cls, win)
            if new_tower_position_items:
                rect_idx = new_tower_position_items[0]
                old = cls.grid.array_2d[rect_idx[1]][rect_idx[0]]
                cls.grid.array_2d[rect_idx[1]][rect_idx[0]] = "t"
                if cls.grid.get_path():
                    tower_class.builded_towers.append(
                        tower_class(new_tower_position_items[1], new_tower_position_items[2])
                    )
                    cls.money -= tower_class.PRICE
                else:
                    print(cls.grid.array_2d)
                    cls.grid.array_2d[rect_idx[1]][rect_idx[0]] = old

    @classmethod
    def start_battle_phase(cls):
        cls.counter -= 1
        if cls.counter <= -1:
            cls.counter = cls.time_of_prepare_phase
            cls.phase = "battle"
            if cls.wave_num < len(waves_of_enemies):
                cls.enemies_to_spawn, spawn_delay = waves_of_enemies[cls.wave_num]
                pygame.time.set_timer(cls.SPAWN_ENEMY_EVENT, spawn_delay)
                cls.wave_num += 1
            else:
                cls.phase = "won"

    @classmethod
    def spawn_enemies(cls):
        if pygame.event.get(cls.SPAWN_ENEMY_EVENT) and len(cls.enemies_to_spawn) > 0:
            new_enemy_class = cls.enemies_to_spawn[0]
            cls.enemies_to_spawn.pop(0)
            cls.enemies.append(new_enemy_class(cls.grid.get_path()))
