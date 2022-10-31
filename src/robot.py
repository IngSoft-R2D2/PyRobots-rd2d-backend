from __future__ import annotations
from constants import *
import random
import math
import time

class Robot:
    direction: int
    velocity: int
    __position: tuple[float,float]
    __damage: int
    __wall_collision: bool
    __cannon_degree: int
    __cannon_distance: float
    __reload_time_counter: float
    __scanner_direction: int
    __resolution: int
    __scann_result: float


    def __init__(self):
        self.__position = (random.randint(FIRST_COORD,LAST_COORD), random.randint(FIRST_COORD,LAST_COORD))
        self.__wall_collision = False

    def get_direction(self):
        return self.direction

    def get_velocity(self):
        return self.velocity

    def get_position(self):
        return self.__position

    def get_damage(self):
        return self.__damage
    
    def is_cannon_ready(self):
        elapsed_time_since_start_reload = time.perf_counter() - self.__reload_time_counter
        return elapsed_time_since_start_reload >= RELOAD_TIME

    def cannon(self, degree: int, distance: float):
        self.__cannon_degree = degree
        self.__cannon_distance = distance

    def point_scanner(self, direction: int, resolution: int):
        self.__scanner_direction = direction
        self.__resolution = resolution

    def scanned(self):
        return self.__scann_result

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
        y = sen * ((VELOCITY*self.get_velocity())/100)
        x = math.sqrt(((VELOCITY*self.get_velocity())/100)**2-y**2)
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

    def __scann(self, list_of_robots: list[Robot]):
        (x1,y1) = self.get_position()
        dist = float('inf')
        for robot in list_of_robots:
            (x2,y2) = robot.get_position()
            if (x2-x1) != 0:
                m = (y2 - y1)/(x2-x1)
                if m > 0:
                    if x2 >= x1 and y2 >= y1:
                        theta = math.degrees(math.atan(m))
                    if x2 <= x1 and y2 <= y1:
                        theta = math.degrees(math.atan(m))+180
                if m < 0:
                    if x2 <= x1 and y2 >= y1:
                        theta = math.degrees(math.atan(m))+180
                    if x2 >= x1 and y2 <= y1:
                        theta = math.degrees(math.atan(m))+360
                if m == 0:
                    if x2 > x1:
                        theta = 0
                    if x2 < x1:
                        theta = 180
                print(m)
            else:
                if (y2 > y1):
                    theta = 90
                elif (y2 < y1):
                    theta = 270
            if (self.__scanner_direction-self.__resolution < 0):
                right = 360 + self.__scanner_direction-self.__resolution
                if not (self.__scanner_direction+self.__resolution < theta < right):
                    d =  math.sqrt((x2-x1)**2+(y2-y1)**2)
                    if d < dist:
                        dist = d
            elif (self.__scanner_direction+self.__resolution > 359):
                left = 360 - self.__scanner_direction+self.__resolution
                if not (left < theta < self.__scanner_direction-self.__resolution):
                    d =  math.sqrt((x2-x1)**2+(y2-y1)**2)
                    if d < dist:
                        dist = d
            elif (self.__scanner_direction-self.__resolution <= theta <= self.__scanner_direction+self.__resolution):
                d =  math.sqrt((x2-x1)**2+(y2-y1)**2)
                if d < dist:
                    dist = d
        self.__scann_result = dist

    def __attack(self, robot: Robot):
        target = self.scanned()
        if (self.is_cannon_ready()):
            # attack !!!
            pass
        # Start reload time after the shoot.
        self.__reload_time_counter = time.perf_counter()