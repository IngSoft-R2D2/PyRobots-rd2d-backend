from pony.orm import *
from robot import *

def round(robots: "list[Robot]") -> dict:
    round_json = {}

    not_dead_robots = robots[:]
    for bot in robots:
        if bot.get_damage() == 100:
            not_dead_robots.remove(bot)

    for bot in not_dead_robots:
        bot.respond()

    for bot in not_dead_robots:
        robots_to_scann = not_dead_robots[:]
        robots_to_scann.remove(bot)
        bot._Robot__scann(robots_to_scann)

    for bot in not_dead_robots:
        bot._Robot__attack(not_dead_robots)

    for bot in robots:
        bot_name = bot._Robot__get_name()
        round_json[bot_name] = {}
        round_json[bot_name]['position'] = bot.get_position()

    for bot in robots:
        missile = bot._Robot__get_missile()
        bot_name = bot._Robot__get_name()
        round_json[bot_name]['missile'] = missile

    for bot in not_dead_robots:
        bot._Robot__move()

    for bot in not_dead_robots:
        robots_collision = not_dead_robots[:]
        robots_collision.remove(bot)
        bot._Robot__check_collision(robots_collision)

    for bot in robots:
        bot_name = bot._Robot__get_name()
        round_json[bot_name]['damage'] = bot.get_damage()

    return round_json

def game(number_of_rounds: int, robots: "list[Robot]") -> dict:
    game_json = {}
    for bot in robots:
        bot.initialize()
        bot._Robot__set_damage(0)
    for round_index in range(number_of_rounds):
        key = "round_" + str(round_index)
        game_json[key] = round(robots)
        robots_amount = len(robots)
        dead_robots = 0
        for bot in robots:
            if (bot.get_damage() == 100):
                dead_robots += 1
        if  dead_robots >= robots_amount-1:
            break
    return game_json
