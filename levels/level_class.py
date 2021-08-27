import pygame
from grid.grid import Grid
from game.colors import ColorsRGB
from game.button import Button
from towers.tower import Tower
from enemies.enemy import Enemy
from enemies.waves import waves_of_enemies


class Level:
    grid = Grid()
    towers_to_buy = [
        Tower
    ]
    builded_towers = []
    enemies = []
    waiting_enemies = []

    pygame.time.set_timer(pygame.USEREVENT, 1000)  # One second
    time_of_prepare_phase = 10
    counter = time_of_prepare_phase
    phase = "prepare"

    money = 30
    lives = 50
    REWARD = 5
    wave_num = 0

    @classmethod
    def draw(cls, win):
        win.fill(ColorsRGB.GREY)
        pygame.draw.rect(win, ColorsRGB.BROWN, (1430, 250, 240, 650), 0, 10)
        if cls.phase == "prepare":
            Button(1430, 40, 240, 20, ColorsRGB.GREY,
                   text=f"Time to battle: {cls.counter}",
                   font_size=33, border=False, font_color=ColorsRGB.WHITE).draw(win)
        Button(1430, 200, 240, 20, ColorsRGB.GREY,
               text=f"Money: {cls.money}", font_size=30, border=False, font_color=ColorsRGB.YELLOW).draw(win)
        Button(1430, 250, 240, 20, ColorsRGB.GREY,
               text=f"Allowed Escapes: {cls.lives}", font_size=20, border=False, font_color=ColorsRGB.RED).draw(win)

        Tower.draw_buttons(win)
        cls.grid.draw(win)

        if cls.phase == "battle":
            Button(1430, 40, 240, 20, ColorsRGB.GREY,
                   text=f"WAVE: {cls.wave_num}",
                   font_size=33, border=False, font_color=ColorsRGB.YELLOW).draw(win)
            Button(1430, 140, 240, 20, ColorsRGB.GREY,
                   text=f"Living enemies: {len(cls.enemies)}",
                   font_size=25, border=False, font_color=ColorsRGB.DARK_RED).draw(win)
            cls.spawn_enemies()

            order = cls.draw_and_move_enemies(win)
            if len(cls.enemies) == 0:
                cls.phase = "prepare"
                if len(waves_of_enemies) <= 0:
                    cls.phase = "won"
            if order == "destroyed":
                cls.money += cls.REWARD
            elif order == "out":
                cls.lives -= 1
                if cls.lives <= 0:
                    cls.phase = "lost"
            Tower.search_for_enemies(cls.builded_towers, cls.enemies)

        elif cls.phase == "won":
            Button(720, 440, 0, 0, ColorsRGB.YELLOW,
                   text="YOU WON", font_size=100, border=False, font_color=ColorsRGB.GREEN).draw(win)
        elif cls.phase == "lost":
            Button(720, 440, 0, 0, ColorsRGB.YELLOW,
                   text="YOU LOST", font_size=100, border=False, font_color=ColorsRGB.RED).draw(win)

        for tower in cls.builded_towers:
            tower.draw_on_grid(win, cls.grid.square_size+5)

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
                if not is_enemy_moving:
                    order = "out"
        return order

    @classmethod
    def buttons_events(cls, win):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1

            if event.type == pygame.USEREVENT and cls.phase == "prepare":
                cls.start_battle_phase()
            if cls.phase == "prepare" and cls.money >= Tower.PRICE:
                Tower.add_button.is_active = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    cls.build_new_tower(win)
            else:
                Tower.add_button.is_active = False

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
                    cls.grid.array_2d[rect_idx[1]][rect_idx[0]] = "t"
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
            cls.phase = "battle"
            if len(waves_of_enemies) > 0:
                cls.waiting_enemies = waves_of_enemies[0]()
                waves_of_enemies.pop(0)
                cls.wave_num += 1
            else:
                cls.phase = "won"

    @classmethod
    def spawn_enemies(cls):
        for waiting_enemy in cls.waiting_enemies:
            is_ready = waiting_enemy.waiting()
            if is_ready:
                cls.enemies.append(Enemy(cls.grid.get_path()))
                cls.waiting_enemies.remove(waiting_enemy)
