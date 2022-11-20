from __future__ import annotations
from constants import *
import random
import math
import time
from typing import List

class Missile:

    def __init__(self, total_distance, degree, initial_position, owner, id):
        self.__total_distance = total_distance
        self.__degree = degree
        self.__actual_position = initial_position
        self.__distance_traveled = 0
        self.__hit_ground = total_distance == 0
        self.__stopped = False
        self.__wall_collision = False
        self.__owner = owner
        self.__id = id

    def get_id(self):
        return self.__id

    def get_position(self):
        return self.__actual_position

    def get_owner(self):
        return self.__owner

    def is_stopped(self):
        return self.__stopped

    def move_missile(self):
        if not self.__stopped and self.__distance_traveled < self.__total_distance:
            if self.__distance_traveled + MISSILE_VELOCITY < self.__total_distance:
                self.__actual_position = self.__calculate_missile_position(self.__actual_position, MISSILE_VELOCITY)
                self.__distance_traveled += MISSILE_VELOCITY
            else:
                remaining_distance_before_explotion = self.__total_distance - self.__distance_traveled
                self.__actual_position = self.__calculate_missile_position(self.__actual_position,
                                                                           remaining_distance_before_explotion)
                self.__distance_traveled += remaining_distance_before_explotion
                self.__hit_ground = True

    def __inflict_damage(self, damage: int, robot: Robot):
        if (0 <= damage <= 100):
            if ((robot.get_damage() + damage) <= 100):
                robot._Robot__set_damage(robot.get_damage() + damage)
            else:
                robot._Robot__set_damage(100)

    def inflict_missile_damage(self, robots: List[Robot]):
        if (self.__hit_ground or self.__wall_collision) and not self.__stopped:
            robots_damage_5_meters: List[Robot] = get_robots_in_range(
                robots,
                self.__actual_position,
                (0,5)
            )
            robots_damage_20_meters: List[Robot] = get_robots_in_range(
                robots,
                self.__actual_position,
                (5,20)
            )
            robots_damage_40_meters: List[Robot] = get_robots_in_range(
                robots,
                self.__actual_position,
                (20,40)
            )
            for robot in robots_damage_5_meters:
                self.__inflict_damage(MISSILE_DAMAGE_5_METERS, robot)
            for robot in robots_damage_20_meters:
                self.__inflict_damage(MISSILE_DAMAGE_20_METERS, robot)
            for robot in robots_damage_40_meters:
                self.__inflict_damage(MISSILE_DAMAGE_40_METERS, robot)
            self.__stopped = True

    def __calculate_missile_position(
        self,
        initial_position: tuple[int, int],
        shooting_distance: int
    ) -> tuple[int, int]:
        if (self.__degree >= 0 and self.__degree <=90):
            alpha = self.__degree
        elif (self.__degree > 90 and self.__degree <= 180):
            alpha = 180 - self.__degree
        elif (self.__degree > 180 and self.__degree <= 270):
            alpha = self.__degree - 180
        else:
            alpha = 360 - self.__degree
        sen = math.sin(math.radians(alpha))
        y = sen * shooting_distance
        x = math.sqrt(shooting_distance**2-y**2)
        if (self.__degree >= 0 and self.__degree <= 90):
            x_axis = initial_position[0] + x
            y_axis = initial_position[1] + y
        elif (self.__degree > 90 and self.__degree <= 180):
            x_axis = initial_position[0] - x
            y_axis = initial_position[1] + y
        elif (self.__degree > 180 and self.__degree <= 270):
            x_axis = initial_position[0] - x
            y_axis = initial_position[1] - y
        else:
            x_axis = initial_position[0] + x
            y_axis = initial_position[1] - y
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
        return (x_axis,y_axis)

class Robot:
    __direction: int
    __velocity: int
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

    def __init__(self, name: str, id: int):
        self.__name = name
        self.__id = id
        self.__direction = random.randint(0,359)
        self.__velocity = random.randint(1,VELOCITY)
        self.__position = (random.randint(FIRST_COORD,LAST_COORD), random.randint(FIRST_COORD,LAST_COORD))
        self.__damage = 0
        self.__cannon_degree = random.randint(0,359)
        self.__cannon_distance = round(random.uniform(0,CANNON_RANGE), 2)
        self.__reload_time_counter = time.perf_counter()
        self.__wall_collision = False
        self.__scanner_direction = random.randint(0,359)
        self.__resolution = 0
        self.__scann_result = float('inf')
        self.__number_of_missiles = 0

    def get_direction(self):
        return self.__direction

    def get_velocity(self):
        return self.__velocity

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
        self.__direction = direction
        self.__velocity = velocity

    def __get_name(self):
        return self.__name

    def __get_id(self):
        return self.__id

    def __move(self):
        if (self.get_direction() >= 0 and self.get_direction() <=90):
            alpha = self.get_direction()
        elif (self.get_direction() > 90 and self.get_direction() <= 180):
            alpha = 180 - self.get_direction()
        elif (self.get_direction() > 180 and self.get_direction() <= 270):
            alpha = self.get_direction() - 180
        else:
            alpha = 360 - self.get_direction()
        sen = math.sin(math.radians(alpha))
        y = sen * ((VELOCITY*self.get_velocity())/100)
        x = math.sqrt(((VELOCITY*self.get_velocity())/100)**2-y**2)
        if (self.get_direction() >= 0 and self.get_direction() <= 90):
            x_axis = self.get_position()[0]+x
            y_axis = self.get_position()[1]+y
        elif (self.get_direction() > 90 and self.get_direction() <= 180):
            x_axis = self.get_position()[0]-x
            y_axis = self.get_position()[1]+y
        elif (self.get_direction() > 180 and self.get_direction() <= 270):
            x_axis = self.get_position()[0]-x
            y_axis = self.get_position()[1]-y
        else:
            x_axis = self.get_position()[0]+x
            y_axis = self.get_position()[1]-y
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

    def __scann(self, list_of_robots: List[Robot]):
        (x1,y1) = self.get_position()
        dist = float('inf')
        for robot in list_of_robots:
            (x2,y2) = robot.get_position()
            if (x2-x1) != 0:
                m = (y2 - y1)/(x2-x1)
                if m > 0:
                    if x2 > x1 and y2 > y1:
                        theta = math.degrees(math.atan(m))
                    elif x2 < x1 and y2 < y1:
                        theta = math.degrees(math.atan(m))+180
                elif m < 0:
                    if x2 < x1 and y2 > y1:
                        theta = math.degrees(math.atan(m))+180
                    elif x2 > x1 and y2 < y1:
                        theta = math.degrees(math.atan(m))+360
                else:
                    if x2 > x1:
                        theta = 0
                    elif x2 < x1:
                        theta = 180
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

    def __inflict_collision_damage(self):
        if ((self.get_damage() + COLLISION_DAMAGE) <= 100):
            self.__damage = self.get_damage() + COLLISION_DAMAGE
        else:
            self.__damage = 100

    def __attack(self, robots: List[Robot], missiles: List[Missile]):
        if (self.is_cannon_ready()):
            # Generate missile
            self.__number_of_missiles += 1
            missile_id = "missile_" + str(self.__number_of_missiles) + "_" + self.__get_name()
            new_missile = Missile(self.__cannon_distance, self.__cannon_degree,
                                  self.get_position(), self.__get_name(), missile_id)
            missiles.append(new_missile)
            # start reload time
            self.__reload_time_counter = time.perf_counter()

    def __check_collision(self, robots: List[Robot]):
        robots_collision = get_robots_in_range(robots, self.get_position(), (0,5))
        for _ in range(len(robots_collision)):
            self.__inflict_collision_damage()
        if self.__wall_collision:
            self.__inflict_collision_damage()
            self.__wall_collision = False

    def __set_damage(self, damage):
        self.__damage = damage


def get_robots_in_range(
        robots: List[Robot],
        position: tuple[int, int],
        circle_area: tuple[int, int]
    ) -> List[Robot]:
    (x1,y1) = position
    robots_result: List[Robot] = []
    for robot in robots:
        (x2,y2) = robot.get_position()
        d = math.sqrt((x2-x1)**2+(y2-y1)**2)
        if (d >= circle_area[0] and d < circle_area[1]):
            robots_result.append(robot)
    return robots_result