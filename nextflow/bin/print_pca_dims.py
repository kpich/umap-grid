#!/usr/bin/env python

import argparse

import pandas as pd


N = [0, 10, 20, 50, 100, 200, 500]


def print_pca_dims(data):
    data_df = pd.read_csv(data)
    max_n = len(data_df)

    for n in N:
        if n < max_n:
            print(n)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True)
    args = parser.parse_args()
    print_pca_dims(data=args.data)
