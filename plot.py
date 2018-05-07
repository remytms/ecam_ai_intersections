#! /usr/bin/python3
# -*- coding: utf-8 -*-


import collections
import numpy as np
import matplotlib as mtplt
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import data


def plot_cluster(clusters=[]):
    assert(len(clusters) > 0)
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for cluster in clusters:
        ax.add_patch(
            patches.Rectangle(
                (cluster[1], 0),
                cluster[2] - cluster[1],
                1,
                fill=False,
            )
        )
        ax.set_xlim(0, clusters[-1][2])
        ax.set_ylim(0, 2)
    plt.show()


def plot(inputs, outputs):
    assert(len(inputs) > 0)
    assert(len(outputs) > 0)
    fig = plt.figure()
    data = inputs + outputs

    size = len(inputs) + len(outputs)

    max_time = 0
    for datum in data:
        for cluster in datum:
            if cluster[2] > max_time:
                max_time = cluster[2]

    for i in range(size):
        ax = fig.add_subplot((size * 100) + 10 + (i + 1))
        for cluster in data[i]:
            ax.add_patch(
                patches.Rectangle(
                    (cluster[1], 0),
                    cluster[2] - cluster[1],
                    1,
                    fill=False,
                )
            )
            ax.set_xlim(0, max_time)
            ax.set_ylim(0, 2)
    plt.show()


if __name__ == "__main__":
    test_clusters = data.import_data('test.csv')
    plot_cluster(test_clusters)
