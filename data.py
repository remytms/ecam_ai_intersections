#! /usr/bin/python3
# -*- coding: utf-8 -*-


from numpy import genfromtxt


class Cluster:
    """
    Represent a cluster with:
        - vehicle density
        - arrival time
        - depart time
        - total waiting time
    """

    def __init__(self, data=None, cars=0, intime=0, outtime=0, waittime=0):
        if data is None:
            self.cars = cars
            self.in_time = intime
            self.out_time = outtime
            self.wait_time = waittime
        else:
            self.cars = data[0]
            self.in_time = data[1]
            self.out_time = data[2]
            self.wait_time = data[3]

    def duration(self):
        return self.out_time - self.in_time

    def tolist(self):
        return [
            self.cars,
            self.in_time,
            self.out_time,
            self.wait_time,
        ]

    def __str__(self):
        return "cars: %d, in: %d, out: %d, wait: %d" % (
            self.cars, self.in_time, self.out_time, self.wait_time
        )

    def __repr__(self):
        return "<Cluster cars: %d, in: %d, out: %d, wait: %d>" % (
            self.cars, self.in_time, self.out_time, self.wait_time
        )


def import_data(file):
    """Import data"""
    data = []
    data = genfromtxt(file, delimiter=';').tolist()
    return data


def import_cluster(file):
    """Import data as cluster"""
    data = import_data(file)
    clusters = []
    for cluster in data:
        clusters.append(
            Cluster(cluster)
        )
    return clusters


if __name__ == "__main__":
    print(import_data('test.csv'))
    print(import_cluster('test.csv'))
