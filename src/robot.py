from constants import *
import random

class Robot:
    direction: int
    velocity: int
    __position: int
    __damage: int

    def __init__(self):
        self.__position = (random.randint(FIRST_COORD,LAST_COORD), random.randint(FIRST_COORD,LAST_COORD))

    def get_direction(self):
        return self.__direction

    def get_velocity(self):
        return self.__velocity

    def get_position(self):
        return self.__position

    def get_damage(self):
        return self.__damage

    def drive(self, direction: int, velocity: int):
        self.__direction = direction
        self.__velocity = velocity