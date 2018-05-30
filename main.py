#! /usr/bin/python3
# -*- coding: utf-8 -*-

from copy import deepcopy

from data import import_data, import_cluster
import plot
from fcfs_intersection import FCFSIntersection
from simple_intersection import SimpleIntersection


def main():
    inputs = [[], []]
    inputs[0] = import_data('inputs/input1.csv')
    inputs[1] = import_data('inputs/input2.csv')
    intersec = FCFSIntersection(deepcopy(inputs))
    intersec.run()
    print(intersec.outputs)
    plot.plot(inputs, intersec.outputs)

    inputs[0] = import_cluster('inputs/input1.csv')
    inputs[1] = import_cluster('inputs/input2.csv')
    intersec = SimpleIntersection(deepcopy(inputs))
    intersec.run()
    intersec.print_outputs()
    plot.newplot(inputs, intersec.outputs)


if __name__ == "__main__":
    main()
