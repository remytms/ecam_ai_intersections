#! /usr/bin/python3
# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import matplotlib.patches as patches

from data import import_clusters


def plot_cluster(clusters=None):
    assert clusters
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for cluster in clusters:
        ax.add_patch(
            patches.Rectangle(
                (cluster.in_time, 0),
                cluster.out_time - cluster.in_time,
                1,
                fill=False,
            )
        )
        ax.set_xlim(0, clusters[-1][2])
        ax.set_ylim(0, 2)
    plt.show()


def plot(inputs, outputs):
    assert inputs
    assert outputs
    fig = plt.figure()
    data = inputs + outputs

    size = len(inputs) + len(outputs)

    max_time = 0
    for datum in data:
        for cluster in datum:
            if cluster.out_time > max_time:
                max_time = cluster.out_time

    for i in range(size):
        ax = fig.add_subplot((size * 100) + 10 + (i + 1))
        for cluster in data[i]:
            ax.add_patch(
                patches.Rectangle(
                    (cluster.in_time, 0),
                    cluster.out_time - cluster.in_time,
                    1,
                    fill=False,
                )
            )
            ax.set_xlim(0, max_time)
            ax.set_ylim(0, 2)
    plt.show()


if __name__ == "__main__":
    test_clusters = import_clusters('test.csv')
    plot_cluster(test_clusters)
