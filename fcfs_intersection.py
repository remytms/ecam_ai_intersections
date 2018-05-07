#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""FCFS Intersection

Maintainer: Rémy Taymans <14291@student.ecam.be>
            Christophe Degrelle <11033@student.ecam.be>
Creation: 16 avr 2018
"""


class FCFSIntersection():
    """
    """

    def __init__(self, inputs=[[], []], yellow_delay=10,
                 startup_lost_time=10):
        self.inputs = inputs
        self.yellow_delay = yellow_delay
        self.startup_lost_time = startup_lost_time
        # init
        self.outputs = [[], []]
        self.open = [True, False]
        self.time_last_cluster = 0

    def run(self):
        while self.inputs[0] or self.inputs[1]:
            self.add_delay()

    def sum_outputs(self):
        pass

    def select_next_cluster(self):
        choosen_cluster = []
        choosen_input = -1
        choosen_cluster_index = -1
        for i_idx, inpt in enumerate(self.inputs):
            for c_idx, cluster in enumerate(inpt):
                if choosen_cluster:
                    if (cluster[1] < choosen_cluster[1]
                            or (cluster[1] == choosen_cluster[1]
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

    def add_delay(self):
        cluster, way = self.select_next_cluster()
        if self.time_last_cluster > cluster[1]:
            waiting_time = self.time_last_cluster - cluster[1]
            cluster[1] += waiting_time
            cluster[2] += waiting_time
            cluster[3] += waiting_time
        if self.open[way]:
            self.outputs[way].append(cluster)
        else:
            self.switch_open()
            cluster[1] += self.yellow_delay + self.startup_lost_time
            cluster[2] += self.yellow_delay + self.startup_lost_time
            self.outputs[way].append(cluster)
        self.time_last_cluster = cluster[2]


    def switch_open(self):
        self.open[0] = not self.open[0]
        self.open[1] = not self.open[1]


if __name__ == "__main__":
    pass
