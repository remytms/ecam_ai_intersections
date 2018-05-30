#! /usr/bin/python3
# -*- coding: utf-8 -*-

from copy import deepcopy

from data import import_clusters
from intersection import FixedIntersection, FCFSIntersection
import plot


def main():
    """Tests different algorithm for the same set of data"""
    inputs = [[], []]
    inputs[0] = import_clusters('inputs/input1.csv')
    inputs[1] = import_clusters('inputs/input2.csv')
    intersec = FCFSIntersection(deepcopy(inputs))
    intersec.run()
    intersec.print_outputs()
    plot.plot(inputs, intersec.outputs)

    inputs[0] = import_clusters('inputs/input1.csv')
    inputs[1] = import_clusters('inputs/input2.csv')
    intersec = FixedIntersection(deepcopy(inputs))
    intersec.run()
    intersec.print_outputs()
    plot.plot(inputs, intersec.outputs)


if __name__ == "__main__":
    main()
