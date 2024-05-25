#!/usr/bin/env python

import argparse

import pandas as pd
from sklearn.decomposition import PCA
import umap


def _get_input_embeds(df):
    embed_cols = [col for col in df.columns if col.startswith("dim_")]
    return df[embed_cols].values


def gen_umap(data, seed, n_neighbors, min_dist, pca_dims, metric, csv_outfile):
    data_df = pd.read_csv(data)

    # float<num_examples, embed_dim>.
    input_embeds = _get_input_embeds(data_df)

    if pca_dims:
        pca = PCA(n_components=pca_dims, random_state=seed)
        # float<num_examples, pca_dims>
        input_embeds = pca.fit_transform(input_embeds)

    reducer = umap.UMAP(
        min_dist=min_dist,
        n_neighbors=n_neighbors,
        metric=metric,
        random_state=seed,
    )

    # float<num_examples, 2>.
    umap_embeddings = reducer.fit_transform(input_embeds)

    df = pd.DataFrame(
        {
            "umap_0": umap_embeddings[:, 0],
            "umap_1": umap_embeddings[:, 1],
        }
    )
    df.to_csv(csv_outfile, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--n_neighbors", type=int, required=True)
    parser.add_argument("--min_dist", type=float, required=True)
    parser.add_argument("--pca_dims", type=int, required=True)
    parser.add_argument("--metric", type=int, required=True)
    parser.add_argument("--csv_outfile", type=str, required=True)
    args = parser.parse_args()
    gen_umap(
        data=args.data,
        seed=args.seed,
        n_neighbors=args.n_neighbors,
        min_dist=args.min_dist,
        pca_dims=args.pca_dims,
        metric=args.metric,
        csv_outfile=args.csv_outfile,
    )
