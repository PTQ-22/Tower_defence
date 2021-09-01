from .enemy import Enemy
from .vehicle_enemy import VehicleEnemy
from .big_enemy import BigEnemy

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
    enemies = [BigEnemy, Enemy, VehicleEnemy]
    return enemies, 250


@append_to_waves
def wave_2():
    return [Enemy for _ in range(8)], 200


@append_to_waves
def wave_3():
    return [Enemy for _ in range(19)], 300


@append_to_waves
def wave_4():
    return [Enemy for _ in range(30)], 200


@append_to_waves
def wave_5():
    return [Enemy for _ in range(50)], 100


@append_to_waves
def wave_6():
    return [Enemy for _ in range(100)], 70


@append_to_waves
def wave_7():
    return [Enemy for _ in range(200)], 30


@append_to_waves
def wave_8():
    return [Enemy for _ in range(300)], 20


@append_to_waves
def wave_9():
    return [Enemy for _ in range(500)], 10
