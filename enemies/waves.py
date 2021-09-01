from .enemy import Enemy
from .vehicle_enemy import VehicleEnemy
from .big_enemy import BigEnemy
from .fly_enemy import FlyEnemy

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
    return [Enemy for _ in range(4)], 250


@append_to_waves
def wave_2():
    return [Enemy for _ in range(8)], 200


@append_to_waves
def wave_3():
    enemies = [Enemy for _ in range(15)]
    enemies.append(VehicleEnemy)
    return enemies, 300


@append_to_waves
def wave_4():
    enemies = [Enemy for _ in range(30)]
    enemies.append(FlyEnemy)
    return enemies, 200


@append_to_waves
def wave_5():
    enemies = [VehicleEnemy]
    for _ in range(50):
        enemies.append(Enemy)
    enemies.append(FlyEnemy)
    return enemies, 100


@append_to_waves
def wave_6():
    enemies = [BigEnemy]
    for _ in range(80):
        enemies.append(Enemy)
    for _ in range(5):
        enemies.append(VehicleEnemy)
    return enemies, 200


@append_to_waves
def wave_7():
    enemies = [BigEnemy, VehicleEnemy]
    for _ in range(20):
        enemies.append(Enemy)
    enemies.append(VehicleEnemy)
    for _ in range(30):
        enemies.append(Enemy)
    for _ in range(10):
        enemies.append(FlyEnemy)
    for _ in range(5):
        enemies.append(BigEnemy)
    return enemies, 100


@append_to_waves
def wave_8():
    return [FlyEnemy for _ in range(100)], 200


@append_to_waves
def wave_9():
    return [BigEnemy for _ in range(200)], 100
