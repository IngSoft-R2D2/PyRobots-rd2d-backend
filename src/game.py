from pony.orm import *
from robot import *
from databaseFunctions import *
from collections import OrderedDict
from typing import (
    List, Dict
)

def round(robots: List[Robot], missiles: List[Missile]) -> dict:
    round_json = {}
    round_json['Robots'] = {}
    round_json['Missiles'] = {}

    not_dead_robots = robots[:]
    for bot in robots:
        if bot.get_damage() == 100:
            not_dead_robots.remove(bot)

    for bot in not_dead_robots:
        try:
            bot.respond()
        except Exception as e:
            bot._Robot__set_damage(100)
            print(f"Invalid robot: id {bot._Robot__get_id()}")
            print(e)

    for bot in not_dead_robots:
        robots_to_scann = not_dead_robots[:]
        robots_to_scann.remove(bot)
        bot._Robot__scann(robots_to_scann)

    for bot in not_dead_robots:
            bot._Robot__attack(not_dead_robots, missiles)

    for m in missiles:
        m.inflict_missile_damage(not_dead_robots)

    for m in missiles:
        missile_key = m.get_id()
        round_json['Missiles'][missile_key] = {}
        round_json['Missiles'][missile_key]['missile_position'] = m.get_position()
        round_json['Missiles'][missile_key]['missile_status'] = m.is_stopped()
        round_json['Missiles'][missile_key]['owner'] = m.get_owner()

    check_explotion = missiles[:]
    for m in check_explotion:
        if m.is_stopped():
            missiles.remove(m)

    for m in missiles:
        m.move_missile()

    for bot in robots:
        bot_name = bot._Robot__get_name()
        round_json['Robots'][bot_name] = {}
        round_json['Robots'][bot_name]['position'] = bot.get_position()

    for bot in not_dead_robots:
        robots_collision = not_dead_robots[:]
        robots_collision.remove(bot)
        bot._Robot__check_collision(robots_collision)

    for bot in not_dead_robots:
        bot._Robot__move()

    for bot in robots:
        bot_name = bot._Robot__get_name()
        round_json['Robots'][bot_name]['damage'] = bot.get_damage()

    return round_json

def competitive_round(robots: List[Robot], missiles: List[Missile]):
    for bot in robots:
        try:
            bot.respond()
        except Exception as e:
            bot._Robot__set_damage(100)
            print(f"Invalid robot: id {bot._Robot__get_id()}")
            print(e)

    for bot in robots:
        robots_to_scann = robots[:]
        robots_to_scann.remove(bot)
        bot._Robot__scann(robots_to_scann)

    for bot in robots:
        bot._Robot__attack(robots, missiles)

    for m in missiles:
        m.inflict_missile_damage(robots)

    check_explotion = missiles[:]
    for m in check_explotion:
        if m.is_stopped():
            missiles.remove(m)

    for m in missiles:
        m.move_missile()

    for bot in robots:
        robots_collision = robots[:]
        robots_collision.remove(bot)
        bot._Robot__check_collision(robots_collision)

    for bot in robots:
        if bot.get_damage() == 100:
            robots.remove(bot)

    for bot in robots:
        bot._Robot__move()


def game(number_of_rounds: int, robots: List[Robot]) -> dict:
    missiles: List[Missile] = []
    game_json = {}
    for bot in robots:
        try:
            bot.initialize()
        except Exception as e:
            bot._Robot__set_damage(100)
            print(f"Invalid robot: id {bot._Robot__get_id()}")
            print(e)
    for round_index in range(1,number_of_rounds+1):
        key = "round_" + str(round_index)
        game_json[key] = round(robots,missiles)
        robots_amount = len(robots)
        dead_robots = 0
        for bot in robots:
            if (bot.get_damage() == 100):
                dead_robots += 1
        if  dead_robots >= robots_amount-1:
            break
    return game_json

def competitive_game(number_of_rounds: int, robots: List[Robot]):
    missiles: List[Missile] = []
    winners = []
    for bot in robots:
        try:
            bot.initialize()
        except Exception as e:
            bot._Robot__set_damage(100)
            print(f"Invalid robot: id {bot._Robot__get_id()}")
            print(e)
    for _ in range(number_of_rounds):
        competitive_round(robots,missiles)
        if len(robots) < 2:
            break
    if len(robots) > 0 :
        for bot in robots:
            winners.append(bot._Robot__get_id())
    return winners

def run_match(db, robots_id: List[int], number_of_games: int, number_of_rounds: int):
    match_results = dict()
    for bot_id in robots_id:
        match_results[bot_id] = {}
        match_results[bot_id]['user_name'] = get_user_creator_by_robot_id(db, bot_id)
        match_results[bot_id]['robot_name'] = get_robot_name_by_id(db, bot_id)
        match_results[bot_id]['won_games'] = 0
    for _ in range(number_of_games):
        robots = generate_robots_for_game(db, robots_id)
        result = competitive_game(number_of_rounds,robots)
        if result != []:
            for robot_id in result:
                match_results[robot_id]['won_games'] += 1

    for bot_id in robots_id:
        match_results[bot_id]['lost_games'] = number_of_games - match_results[bot_id]['won_games']

    match_results_descending = OrderedDict(sorted(match_results.items(), 
                                  key=lambda kv: kv[1]['won_games'], reverse=True))

    return match_results_descending