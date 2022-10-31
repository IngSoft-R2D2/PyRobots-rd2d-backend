from constants import *
import random
import math

class Robot:
    direction: int
    velocity: int
    __position: tuple[float,float]
    __damage: int
    __wall_collision: bool

    def __init__(self):
        self.__position = (500,500)#(random.randint(FIRST_COORD,LAST_COORD), random.randint(FIRST_COORD,LAST_COORD))
        self.__wall_collision = False

    def get_direction(self):
        return self.direction

    def get_velocity(self):
        return self.velocity

    def get_position(self):
        return self.__position

    def get_damage(self):
        return self.__damage

    def drive(self, direction: int, velocity: int):
        self.direction = direction
        self.velocity = velocity

    def __move(self):
        if (self.get_direction() >= 0 and self.get_direction() <=90):
            alpha = self.get_direction()
        elif (self.get_direction() > 90 and self.get_direction() <= 180):
            alpha = 180 - self.get_direction()
        elif (self.get_direction() > 180 and self.get_direction() <= 270):
            alpha = self.get_direction() - 180
        else:
            alpha = 360 -self.get_direction()
        sen = math.sin(math.radians(alpha))
        x = math.sqrt(((VELOCITY*self.get_velocity())/100)**2/(1+sen**2))
        y = sen * x
        if (self.get_direction() == 0):
            x_axis = self.__position[0]+(VELOCITY*self.get_velocity())/100
            y_axis = self.__position[1]
        elif (self.get_direction() == 90):
            x_axis = self.__position[0]
            y_axis = self.__position[1]+(VELOCITY*self.get_velocity())/100
        elif (self.get_direction() == 180):
            x_axis = self.__position[0]-(VELOCITY*self.get_velocity())/100
            y_axis = self.__position[1]
        elif (self.get_direction() == 270):
            x_axis = self.__position[0]
            y_axis = self.__position[1]-(VELOCITY*self.get_velocity())/100
        elif (self.get_direction() > 0 and self.get_direction() < 90):
            x_axis = self.__position[0]+x
            y_axis = self.__position[1]+y
        elif (self.get_direction() > 90 and self.get_direction() < 180):
            x_axis = self.__position[0]-x
            y_axis = self.__position[1]+y
        elif (self.get_direction() > 180 and self.get_direction() < 270):
            x_axis = self.__position[0]-x
            y_axis = self.__position[1]-y
        else:
            x_axis = self.__position[0]+x
            y_axis = self.__position[1]-y
        if x_axis < 0:
            x_axis = 0
            __wall_collision = True
        if y_axis < 0:
            y_axis = 0
            __wall_collision = True
        if y_axis > 999:
            y_axis = 999
            __wall_collision = True
        if x_axis > 999:
            x_axis = 999
            __wall_collision = True
        self.__position = (x_axis,y_axis)
