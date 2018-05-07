#! /usr/bin/python3
# -*- coding: utf-8 -*-


from numpy import genfromtxt


def import_data(file):
    """Import data"""
    data = []
    data = genfromtxt(file, delimiter=';').tolist()
    return data


if __name__ == "__main__":
    print(import_data('test.csv'))
