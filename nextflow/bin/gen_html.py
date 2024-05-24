#!/usr/bin/env python

import argparse
from pathlib import Path

import pandas as pd
from jinja2 import Template


TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>UMAP grid</title>
</head>
<body>
    {% for (n_neighbors, min_distance, seed), group in grouped %}
        <div style="margin-bottom: 20px;">
            <h2>N Neighbors: {{ n_neighbors }}, Min Distance: {{ min_distance }}</h2>
            {% for _, row in group.iterrows() %}
                <div style="margin-top: 10px;">
                    <img src="plots/{{ row.png }}" style="max-width: 1000px;"><br>
                    Seed: {{ row.seed }}<br>
                    Min Distance: {{ row.min_distance }}<br>
                    N Neighbors: {{ row.n_neighbors }}
                </div>
            {% endfor %}
        </div>
    {% endfor %}
</body>
</html>
"""


def _split_line(line):
    fields = [field.strip() for field in line.strip("[]").split(",")]
    fields[0] = Path(fields[0]).name
    return fields


def _get_df(png_data):
    pngs, seeds, n_neighbs, min_dists = [], [], [], []
    for i, line in enumerate(Path(png_data).read_text().split("\n")):
        if not line:
            continue
        fields = _split_line(line)
        if len(fields) != 4:
            raise ValueError(f"Unexpected format line {i}: '{line}'")
        pngs.append(fields[0])
        seeds.append(fields[1])
        n_neighbs.append(fields[2])
        min_dists.append(fields[3])
    return pd.DataFrame(
        {
            "png": pngs,
            "seed": seeds,
            "min_distance": min_dists,
            "n_neighbors": n_neighbs,
        }
    )


def gen_html(png_data, html_outfile):
    df = _get_df(png_data)

    df = df.sort_values(by=["n_neighbors", "min_distance", "seed"])
    grouped = df.groupby(["n_neighbors", "min_distance", "seed"])

    template = Template(TEMPLATE)
    html_output = template.render(grouped=grouped)

    Path(html_outfile).write_text(html_output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--png_data", type=str, required=True)
    parser.add_argument("--html_outfile", type=str, required=True)
    args = parser.parse_args()
    gen_html(png_data=args.png_data, html_outfile=args.html_outfile)
