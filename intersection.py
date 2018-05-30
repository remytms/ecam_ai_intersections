#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""Intersection Algorithm

Maintainer: Rémy Taymans <14291@student.ecam.be>
            Christophe Degrelle <11033@student.ecam.be>
Creation: 16 avr 2018
"""

from abc import ABC, abstractmethod
from math import floor

from data import Cluster


class Intersection(ABC):
    """
    Abstract class for intersections
    """

    def __init__(self, inputs=None, yellow_delay=10,
                 startup_lost_time=5):
        self.inputs = [[], []]
        if inputs is not None:
            self.inputs = inputs
        self.yellow_delay = yellow_delay
        self.startup_lost_time = startup_lost_time
        # init
        self.outputs = [[], []]
        self.open = [True, False]
        self.cur_time = 0

    @abstractmethod
    def select_next_cluster(self):
        """Select the next cluster that will cross the intersection"""
        pass

    @abstractmethod
    def cross(self):
        """
        Make the next cluster cross the intersection and go from the
        input to the output.
        """
        pass

    def run(self):
        """Let cross all the inputs to the outputs"""
        while self.inputs[0] or self.inputs[1]:
            self.cross()

    def print_outputs(self):
        """Print outputs"""
        for idx, way in enumerate(self.outputs):
            print("Way %d:" % idx)
            for clt in way:
                print("    " + str(clt))

    def switch_open(self):
        """Change the open way"""
        self.open[0] = not self.open[0]
        self.open[1] = not self.open[1]


class FixedIntersection(Intersection):
    """
    Intersection is open a fixed amount of time in one direction and a
    fixed amount of time in the other direction. Proportion between the
    time open in one way and the other way is configurable.
    """

    def __init__(self, inputs=None, yellow_delay=10,
                 startup_lost_time=5, total_open_duration=60, percent=.5):
        super().__init__(inputs, yellow_delay, startup_lost_time)
        self.total_open_duration = total_open_duration
        # init
        self.open_duration = [total_open_duration * percent,
                              total_open_duration * (1 - percent)]
        self.open_cur_duration = 0

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

    def cross(self):
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

    def idx_open(self):
        """Return the index of the open way"""
        return self.open.index(True)

    def time_before_switch(self):
        """Compute the time left before the next switch in open ways"""
        return self.open_duration[self.idx_open()] - self.open_cur_duration


class FCFSIntersection(Intersection):
    """
    First Come First Serve intersection without prehension.
    It change only when cars are detected in a way. It doesn't look
    ahead to anticipate the change of open way.
    """

    def select_next_cluster(self):
        choosen_cluster = None
        choosen_input = -1
        choosen_cluster_index = -1
        for i_idx, inpt in enumerate(self.inputs):
            for c_idx, cluster in enumerate(inpt):
                if choosen_cluster:
                    if (cluster.in_time < choosen_cluster.in_time
                            or (cluster.in_time == choosen_cluster.in_time
                                and self.open[i_idx])):
                        choosen_cluster = cluster
                        choosen_input = i_idx
                        choosen_cluster_index = c_idx
                else:
                    choosen_cluster = cluster
                    choosen_input = i_idx
                    choosen_cluster_index = c_idx
        del self.inputs[choosen_input][choosen_cluster_index]
        return choosen_cluster, choosen_input

    def cross(self):
        cluster, way = self.select_next_cluster()
        if self.cur_time > cluster.in_time:
            waiting_time = self.cur_time - cluster.in_time
            cluster.in_time += waiting_time
            cluster.out_time += waiting_time
            cluster.wait_time += waiting_time
        if self.open[way]:
            self.outputs[way].append(cluster)
        else:
            self.switch_open()
            cluster.in_time += self.yellow_delay + self.startup_lost_time
            cluster.out_time += self.yellow_delay + self.startup_lost_time
            self.outputs[way].append(cluster)
        self.cur_time = cluster.out_time


if __name__ == "__main__":
    pass
