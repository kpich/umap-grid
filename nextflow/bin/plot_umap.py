#!/usr/bin/env python

import argparse

import matplotlib.pyplot as plt
import pandas as pd


def plot_umap(umap_csv, png_outfile):
    df = pd.read_csv(umap_csv)

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.scatter(
        df["umap_0"],
        df["umap_1"],
        s=100,
        color="blue",
        linewidth=0.7,
        alpha=0.5,
    )

    plt.savefig(png_outfile, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--umap_csv", type=str, required=True)
    parser.add_argument("--png_outfile", type=str, required=True)
    args = parser.parse_args()
    plot_umap(umap_csv=args.umap_csv, png_outfile=args.png_outfile)
