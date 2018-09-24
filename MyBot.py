#!/usr/bin/env python
from __future__ import division
from ants import Ants
import os
from antutils import logexcept, DEBUG_LOG, log
import random
from collections import namedtuple


class MyBot:
    def __init__(self):
        self.turn = 0
        self.orders = {}

    def do_setup(self, ants):
        pass

    def ant_distances(self, ants, loc):
        return {ant: ants.distance(ant, loc) for ant in ants.my_ants()}

    def find_goals(self, ants):
        Goal = namedtuple('Goal', 'goal distances')
        foods = [Goal(goal=food, distances=self.ant_distances(ants, food)) for food in ants.food()]
        enemies = [Goal(goal=loc, distances=self.ant_distances(ants, loc)) for loc, owner in ants.enemy_ants()]

        return foods + enemies

    def prioritize_goals(self, goals):
        prioritized = sorted(goals, key=lambda goal: min(goal.distances.values()))

        return prioritized

    def issue_orders(self, ants, orders):
        current_locs = [loc for loc, _ in orders]
        occupied = [loc for loc in ants.my_ants() if loc not in current_locs]

        for ant_loc, dirs in orders:
            for direction in dirs:
                dest = ants.destination(ant_loc, direction)
                if dest not in occupied:
                    ants.issue_order((ant_loc, direction))
                    occupied.append(dest)

    def assign_goals(self, ants):
        goals = self.find_goals(ants)
        orders = []
        while any(map(lambda goal: goal.distances, goals)):
            prioritized_goals = self.prioritize_goals(goals)

            goal_loc, distances = prioritized_goals.pop(0)
            ant_loc = min(distances, key=distances.get)
            direction = ants.direction(ant_loc, goal_loc)
            orders.append((ant_loc, direction))

            for goal in prioritized_goals:
                goal.distances.pop(ant_loc)

            goals = prioritized_goals

        self.issue_orders(ants, orders)

    @logexcept
    def do_turn(self, ants):
        self.turn += 1
        self.assign_goals(ants)


if __name__ == '__main__':
    @logexcept
    def start():
        try:
            os.remove(DEBUG_LOG)
        except OSError:
            pass

        Ants.run(MyBot())

    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    try:
        start()
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
