#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""Simple Intersection

Maintainer: Rémy Taymans <14291@student.ecam.be>
            Christophe Degrelle <11033@student.ecam.be>
Creation: 16 avr 2018
"""

from math import floor

from data import Cluster


class SimpleIntersection():
    """
    50% in one way 50% in the other way.
    """

    def __init__(self, inputs=[[], []], yellow_delay=10,
                 startup_lost_time=5, total_open_duration=60, percent=.5):
        self.inputs = inputs
        self.yellow_delay = yellow_delay
        self.startup_lost_time = startup_lost_time
        self.total_open_duration = total_open_duration
        # init
        self.outputs = [[], []]
        self.open = [True, False]
        self.cur_time = 0
        self.open_duration = [total_open_duration * percent,
                              total_open_duration * (1 - percent)]
        self.open_cur_duration = 0

    def run(self):
        while self.inputs[0] or self.inputs[1]:
            self.add_delay()

    def sum_outputs(self):
        pass

    def select_next_cluster(self):
        choosen_cluster = None
        choosen_input = -1
        if not self.inputs[self.idx_open()]:
            return choosen_cluster, choosen_input
        next_cluster = self.inputs[self.idx_open()][0]
        if next_cluster.in_time < (self.cur_time
                                   + self.time_before_switch()):
            if next_cluster.duration() <= self.time_before_switch():
                choosen_cluster = Cluster(next_cluster.tolist())
                del self.inputs[self.idx_open()][0]
            else:
                choosen_cluster = Cluster()
                choosen_cluster.in_time = next_cluster.in_time
                choosen_cluster.out_time = (next_cluster.in_time
                                            + self.time_before_switch())
                choosen_cluster.cars = floor(
                    choosen_cluster.duration() / next_cluster.duration()
                    * next_cluster.cars
                )
                choosen_cluster.wait_time = next_cluster.wait_time
                next_cluster.cars -= choosen_cluster.cars
                next_cluster.in_time = choosen_cluster.out_time + 1
                if not choosen_cluster.cars:
                    choosen_cluster = None
            choosen_input = self.idx_open()
        return choosen_cluster, choosen_input

    def add_delay(self):
        cluster, way = self.select_next_cluster()
        if cluster is not None:
            if self.cur_time > cluster.in_time:
                waiting_time = self.cur_time - cluster.in_time
                cluster.in_time += waiting_time
                cluster.out_time += waiting_time
                cluster.wait_time += waiting_time
            self.cur_time += cluster.duration()
            self.open_cur_duration += cluster.duration()
            self.outputs[way].append(cluster)
        else:
            self.cur_time += (self.open_duration[self.idx_open()]
                              - self.open_cur_duration)
            self.open_cur_duration = self.open_duration[self.idx_open()]
        if self.open_cur_duration >= self.open_duration[self.idx_open()]:
            self.switch_open()
            self.cur_time += self.yellow_delay + self.startup_lost_time
            self.open_cur_duration = 0

    def switch_open(self):
        self.open[0] = not self.open[0]
        self.open[1] = not self.open[1]

    def idx_open(self):
        return self.open.index(True)

    def time_before_switch(self):
        return self.open_duration[self.idx_open()] - self.open_cur_duration

    def print_outputs(self):
        for idx, way in enumerate(self.outputs):
            print("Way %d:" % idx)
            for clt in way:
                print("    " + str(clt))


if __name__ == "__main__":
    pass
