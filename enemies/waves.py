from .enemy import Enemy

waves_of_enemies = []
"""
WaitingEnemies are objects that lives until they reached 40 x coordinate.

Then real Enemies objects are created.
"""


class WaitingEnemy:
    def __init__(self, x):
        self.x = x

    def waiting(self):
        self.x += Enemy.MOVE_SPEED
        if self.x >= Enemy.START_X:
            return True
        return False


def append_to_waves(func):
    waves_of_enemies.append(func)


@append_to_waves
def wave_1():  # 5 enemies
    enemies = [
        WaitingEnemy(40),
        WaitingEnemy(20),
        WaitingEnemy(0),
        WaitingEnemy(-20),
        WaitingEnemy(-40)
    ]
    return enemies


@append_to_waves
def wave_2():  # 10 enemies
    enemies = [
        WaitingEnemy(40),
        WaitingEnemy(20),
        WaitingEnemy(0),
        WaitingEnemy(-20),
        WaitingEnemy(-40),
        WaitingEnemy(-60),
        WaitingEnemy(-80),
        WaitingEnemy(-100),
        WaitingEnemy(-120),
        WaitingEnemy(-140),
        WaitingEnemy(-160),
    ]
    return enemies


@append_to_waves
def wave_3():  # 15 enemies
    enemies = [
        WaitingEnemy(40),
        WaitingEnemy(20),
        WaitingEnemy(0),
        WaitingEnemy(-20),
        WaitingEnemy(-40),
        WaitingEnemy(-60),
        WaitingEnemy(-80),
        WaitingEnemy(-100),
        WaitingEnemy(-120),
        WaitingEnemy(-140),
        WaitingEnemy(-160),
        WaitingEnemy(-180),
        WaitingEnemy(-200),
        WaitingEnemy(-220),
        WaitingEnemy(-240),
        WaitingEnemy(-260)
    ]
    return enemies


@append_to_waves
def wave_4():  # 15 enemies
    enemies = [
        WaitingEnemy(40),
        WaitingEnemy(20),
        WaitingEnemy(0),
        WaitingEnemy(-20),
        WaitingEnemy(-40),
        WaitingEnemy(-60),
        WaitingEnemy(-80),
        WaitingEnemy(-100),
        WaitingEnemy(-120),
        WaitingEnemy(-140),
        WaitingEnemy(-160),
        WaitingEnemy(-180),
        WaitingEnemy(-200),
        WaitingEnemy(-220),
        WaitingEnemy(-240),
        WaitingEnemy(-260)
    ]
    return enemies

# @append_to_waves
# def wave_5():  # 15 enemies
#     enemies = [
#         WaitingEnemy(35),
#         WaitingEnemy(15),
#         WaitingEnemy(-5),
#         WaitingEnemy(-25),
#         WaitingEnemy(-45),
#         WaitingEnemy(-65),
#         WaitingEnemy(-85),
#         WaitingEnemy(-105),
#         WaitingEnemy(-125),
#         WaitingEnemy(-145),
#         WaitingEnemy(-165),
#         WaitingEnemy(-185),
#         WaitingEnemy(-205),
#         WaitingEnemy(-225),
#         WaitingEnemy(-245),
#         WaitingEnemy(-265),
#         WaitingEnemy(-285),
#         WaitingEnemy(-305),
#         WaitingEnemy(-325),
#         WaitingEnemy(-345),
#         WaitingEnemy(-365)
#     ]
#     return enemies