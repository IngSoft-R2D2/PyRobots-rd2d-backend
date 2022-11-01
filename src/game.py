from robot import *
from typing import (List)


def round(robots: List[Robot]) -> dict:
    for bot in robots:
        bot.respond()
    for bot in robots:
        robots_to_scann = robots[:]
        robots_to_scann.remove(bot)
        bot._Robot__scann(robots_to_scann)
    for bot in robots:
        bot._Robot__attack(robots)
    for bot in robots:
        missile = bot._Robot__get_missile()

    return "something"