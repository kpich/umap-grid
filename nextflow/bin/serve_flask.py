#!/usr/bin/env python

import argparse
from pathlib import Path

from flask import Flask, render_template
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument("--png_data", type=str, required=True)
parser.add_argument("--plot_dir", type=str, required=True)
parser.add_argument("--port", type=int, required=True)
args = parser.parse_args()

app = Flask(__name__, static_folder=args.plot_dir)


def _split_line(line):
    return [field.strip() for field in line.strip("[]").split(",")]


def _get_df(png_data):
    pngs, seeds, n_neighbs, min_dists, pca_dims, dists = [], [], [], [], [], []
    for i, line in enumerate(Path(png_data).read_text().split("\n")):
        if not line:
            continue
        fields = _split_line(line)
        if len(fields) != 5:
            raise ValueError(f"Unexpected format line {i}: '{line}'")
        pngs.append(Path(fields[0]).name)
        seeds.append(fields[1])
        n_neighbs.append(fields[2])
        min_dists.append(fields[3])
        pca_dims.append(fields[4])
        dists.append(fields[5])
    return pd.DataFrame(
        {
            "png": pngs,
            "seed": seeds,
            "min_distance": min_dists,
            "n_neighbors": n_neighbs,
            "pca_dims": pca_dims,
            "distance_metric": dists,
        }
    )


@app.route("/")
def home():
    df = _get_df(args.png_data)

    df = df.sort_values(
        by=["n_neighbors", "min_distance", "pca_dims", "distance_metric", "seed"]
    )
    grouped = df.groupby(["n_neighbors", "min_distance", "pca_dims", "distance_metric"])

    return render_template("index.html", grouped=grouped)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=args.port)
