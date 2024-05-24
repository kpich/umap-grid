#!/usr/bin/env python

import argparse

import pandas as pd


SMALL_N = [
    2,
    5,
    10,
    20,
    50,
]


def print_num_neighbors_vals(data):
    data_df = pd.read_csv(data)
    max_n = len(data_df) // 2

    for n in SMALL_N:
        if n < max_n:
            print(n)

    for n in range(100, max_n + 1, 100):
        print(n)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True)
    args = parser.parse_args()
    print_num_neighbors_vals(data=args.data)
