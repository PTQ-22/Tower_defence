from .enemy import Enemy

waves_of_enemies = []


def append_to_waves(func):
    waves_of_enemies.append(func())


"""
    To make wave write function like this:
    
    @append_to_waves
    def wave():
        return ['enemy_type' for _ in range('how_many: int')], 'time_between_each_enemy_spawn: int (miliseconds)'
"""


@append_to_waves
def wave_1():
    return [Enemy for _ in range(5)], 250


@append_to_waves
def wave_2():
    return [Enemy for _ in range(10)], 200


@append_to_waves
def wave_3():
    return [Enemy for _ in range(20)], 100


@append_to_waves
def wave_4():
    return [Enemy for _ in range(50)], 100


@append_to_waves
def wave_5():
    return [Enemy for _ in range(100)], 70
