#! /usr/bin/python3
# -*- coding: utf-8 -*-

from copy import deepcopy

from data import import_data
import plot
from fcfs_intersection import FCFSIntersection


def main():
    inputs = [[], []]
    inputs[0] = import_data('inputs/input1.csv')
    inputs[1] = import_data('inputs/input2.csv')
    intersec = FCFSIntersection(deepcopy(inputs))
    intersec.run()
    print(intersec.outputs)
    plot.plot(inputs, intersec.outputs)


if __name__ == "__main__":
    main()
