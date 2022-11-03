from __future__ import annotations
from constants import *
import random
import math
import time



class Robot:
    direction: int
    velocity: int
    __name: str
    __position: tuple[float,float]
    __damage: int
    __wall_collision: bool
    __cannon_degree: int
    __cannon_distance: float
    __reload_time_counter: float
    __scanner_direction: int
    __resolution: int
    __scann_result: float
    __missile: tuple[float, float]


    def __init__(self, name: str):
        self.__name = name
        self.direction = random.randint(0,359)
        self.velocity = random.randint(1,VELOCITY)
        self.__position = (random.randint(FIRST_COORD,LAST_COORD), random.randint(FIRST_COORD,LAST_COORD))
        self.__damage = 0
        self.__cannon_degree = random.randint(0,359)
        self.__cannon_distance = round(random.uniform(0,CANNON_RANGE), 2)
        self.__reload_time_counter = RELOAD_TIME
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
        if (0 <= degree <= 359):
            self.__cannon_degree = degree
        if (distance < CANNON_RANGE):
            self.__cannon_distance = distance
        else:
            self.__cannon_distance = CANNON_RANGE

    def point_scanner(self, direction: int, resolution: int):
        self.__scanner_direction = direction
        self.__resolution = resolution

    def scanned(self):
        return self.__scann_result

    def drive(self, direction: int, velocity: int):
        self.direction = direction
        self.velocity = velocity

    def __get_name(self):
        return self.__name

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
        if (self.get_direction() >= 0 and self.get_direction() <= 90):
            x_axis = self.__position[0]+x
            y_axis = self.__position[1]+y
        elif (self.get_direction() > 90 and self.get_direction() <= 180):
            x_axis = self.__position[0]-x
            y_axis = self.__position[1]+y
        elif (self.get_direction() > 180 and self.get_direction() <= 270):
            x_axis = self.__position[0]-x
            y_axis = self.__position[1]-y
        else:
            x_axis = self.__position[0]+x
            y_axis = self.__position[1]-y
        if x_axis < 0:
            x_axis = 0
            self.__wall_collision = True
        elif x_axis > 999:
            x_axis = 999
            self.__wall_collision = True
        if y_axis < 0:
            y_axis = 0
            self.__wall_collision = True
        elif y_axis > 999:
            y_axis = 999
            self.__wall_collision = True

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
                    elif x2 <= x1 and y2 <= y1:
                        theta = math.degrees(math.atan(m))+180
                elif m < 0:
                    if x2 <= x1 and y2 >= y1:
                        theta = math.degrees(math.atan(m))+180
                    elif x2 >= x1 and y2 <= y1:
                        theta = math.degrees(math.atan(m))+360
                else:
                    if x2 > x1:
                        theta = 0
                    elif x2 < x1:
                        theta = 180
                print(m)
            else:
                if (y2 > y1):
                    theta = 90
                elif (y2 < y1):
                    theta = 270
                else:
                    dist = 0
                    break
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

    def __inflict_damage(self, damage: int):
        if (0 <= damage <= 100):
            if ((self.__damage + damage) <= 100):
                self.__damage = self.__damage + damage
            else:
                self.__damage = 100

    def __inflict_collision_damage(self):
        if ((self.__damage + COLLISION_DAMAGE) <= 100):
            self.__damage = self.__damage + COLLISION_DAMAGE
        else:
            self.__damage = 100

    def __attack(self, robots: list[Robot]):
        if (self.is_cannon_ready()):
            explosion_position = get_explosion_position(
                self.__position,
                self.__cannon_degree,
                self.__cannon_distance
            )
            # Generate missile
            self.__missile = explosion_position
            robots_damage_5_meters: list[Robot] = get_robots_in_range(
                robots,
                explosion_position,
                (0,5)
            )
            robots_damage_20_meters: list[Robot] = get_robots_in_range(
                robots,
                explosion_position,
                (5,20)
            )
            robots_damage_40_meters: list[Robot] = get_robots_in_range(
                robots,
                explosion_position,
                (20,40)
            )
            for robot in robots_damage_5_meters:
                robot.__inflict_damage(MISSILE_DAMAGE_5_METERS)
            for robot in robots_damage_20_meters:
                robot.__inflict_damage(MISSILE_DAMAGE_20_METERS)
            for robot in robots_damage_40_meters:
                robot.__inflict_damage(MISSILE_DAMAGE_40_METERS)
            # start reload time
            self.__reload_time_counter = time.perf_counter()

    def __check_collision(self, robots: list[Robot]):
        robots_collision = get_robots_in_range(robots, self.get_position(), (0,5))
        for _ in range(len(robots_collision)):
            self.__inflict_collision_damage()
        if self.__wall_collision:
            self.__inflict_collision_damage()

    def __get_missile(self):
        return self.__missile

    def __set_damage(self, damage):
        self.__damage = damage




def get_explosion_position(
        robot_position: tuple[int, int],
        shooting_degree: int, 
        shooting_distance: int
    ) -> int:
    if (shooting_degree >= 0 and shooting_degree <=90):
        alpha = shooting_degree
    elif (shooting_degree > 90 and shooting_degree <= 180):
        alpha = 180 - shooting_degree
    elif (shooting_degree > 180 and shooting_degree <= 270):
        alpha = shooting_degree - 180
    else:
        alpha = 360 - shooting_degree
        sen = math.sin(math.radians(alpha))
        y = sen * shooting_distance
        x = math.sqrt(shooting_distance**2-y**2)
    if (shooting_degree == 0):
        x_axis = robot_position[0] + shooting_distance
        y_axis = robot_position[1]
    elif (shooting_degree == 90):
        x_axis = robot_position[0]
        y_axis = robot_position[1] + shooting_distance
    elif (shooting_degree == 180):
        x_axis = robot_position[0] - shooting_distance
        y_axis = robot_position[1]
    elif (shooting_degree == 270):
        x_axis = robot_position[0]
        y_axis = robot_position[1] - shooting_distance
    elif (shooting_degree > 0 and shooting_degree < 90):
        x_axis = robot_position[0] + x
        y_axis = robot_position[1] + y
    elif (shooting_degree > 90 and shooting_degree < 180):
        x_axis = robot_position[0] - x
        y_axis = robot_position[1] + y
    elif (shooting_degree > 180 and shooting_degree < 270):
        x_axis = robot_position[0] - x
        y_axis = robot_position[1] - y
    else:
        x_axis = robot_position[0] + x
        y_axis = robot_position[1] - y
    if x_axis < 0:
        x_axis = 0
    if y_axis < 0:
        y_axis = 0
    if y_axis > 999:
        y_axis = 999
    if x_axis > 999:
        x_axis = 999
    return (x_axis,y_axis)

def get_robots_in_range(
        robots: list[Robot],
        position: tuple[int, int],
        circle_area: tuple[int, int]
    ) -> list[Robot]:
    (x1,y1) = position
    robots_result: list[Robot] = []
    for robot in robots:
        (x2,y2) = robot.get_position()
        d = math.sqrt((x2-x1)**2+(y2-y1)**2)
        if (d >= circle_area[0] and d < circle_area[1]):
            robots_result.append(robot)
    return robots_result