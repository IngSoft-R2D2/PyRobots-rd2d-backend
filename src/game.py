from pony.orm import *
from robot import *

def round(robots: list[Robot]) -> dict:
    round_json = {}
    for bot in robots:
        bot.respond()

    for bot in robots:
        robots_to_scann = robots[:]
        robots_to_scann.remove(bot)
        bot._Robot__scann(robots_to_scann)

    for bot in robots:
        bot._Robot__attack(robots)

    for bot in robots:
        bot_name = bot._Robot__get_name()
        round_json[bot_name] = {}
        round_json[bot_name]['position'] = bot.get_position()

    for bot in robots:
        missile = bot._Robot__get_missile()
        round_json[bot_name]['missile'] = missile

    for bot in robots:
        bot._Robot__move()

    for bot in robots:
        robots_collision = robots[:]
        robots_collision.remove(bot)
        bot._Robot__check_collision(robots_collision)

    for bot in robots:
        round_json[bot_name]['damage'] = bot._Robot__get_damage()
        if bot._Robot__get_damage() == 100:
            robots.remove(bot)

    return round_json

def game(number_of_rounds: int, robots: list[Robot]) -> dict:
    game_json = {}
    for round_index in range(number_of_rounds):
        key = "round_" + str(round_index)
        game_json[key] = round(robots)
        if (len(robots)<=1):
            break
    return game_json
