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
def wave_1():
    enemies = [
        WaitingEnemy(40),
        WaitingEnemy(20),
        WaitingEnemy(0),
        WaitingEnemy(-20),
        WaitingEnemy(-40)
    ]
    return enemies


@append_to_waves
def wave_2():
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
def wave_3():
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
