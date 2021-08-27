from .enemy import Enemy

waves_of_enemies = []


def append_to_waves(func):
    waves_of_enemies.append(func())


@append_to_waves
def wave_1():
    enemies = [Enemy for _ in range(5)]
    return enemies


@append_to_waves
def wave_2():
    enemies = [Enemy for _ in range(30)]
    return enemies


@append_to_waves
def wave_3():
    enemies = [Enemy for _ in range(100)]
    return enemies
