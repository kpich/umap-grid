#!/usr/bin/env nextflow

nextflow.enable.dsl=2

params.data = ""
params.num_seeds = 5
params.port = 5000


process GET_NUM_NEIGHBORS_VALS {
    output:
    stdout

    script:
    """
    print_num_neighbors_vals.py \
        --data="${params.data}"
    """
}


process GEN_UMAP {
    input:
    tuple val(seed), val(n_neighbors), val(min_dist)

    output:
    tuple path("umap.csv"), val(seed), val(n_neighbors), val(min_dist)

    script:
    """
    gen_umap.py \
        --data="${params.data}" \
        --seed="${seed}" \
        --n_neighbors="${n_neighbors}" \
        --min_dist="${min_dist}" \
        --csv_outfile="umap.csv"
    """
}


process PLOT_UMAP {
    input:
    tuple path(umap_csv), val(seed), val(n_neighbors), val(min_dist)

    output:
    tuple(path("plot_seed${seed}_nneigh_${n_neighbors}_mindist_${min_dist}.png"),
          val(seed),
          val(n_neighbors),
          val(min_dist))

    publishDir "results/plots", mode: "copy"

    script:
    """
    plot_umap.py \
        --umap_csv="${umap_csv}" \
        --png_outfile="plot_seed${seed}_nneigh_${n_neighbors}_mindist_${min_dist}.png"
    """
}


process SERVE_FLASK {
    debug true

    input:
    path png_data_txt

    script:
    println("Serving at localhost:${params.port}. ctrl-c to exit")
    """
    serve_flask.py \
        --png_data="${png_data_txt}" \
        --plot_dir="${projectDir}/../results/plots/" \
        --port="${params.port}"
    """
}


workflow {
    seeds = channel.from(0..(params.num_seeds - 1))

    GET_NUM_NEIGHBORS_VALS()
    nneighbors = GET_NUM_NEIGHBORS_VALS.out.splitText().map { it.trim() }

    min_dists = Channel.of(0.0,  0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 0.8, 0.9, 0.99)

    hparams = seeds.combine(nneighbors).combine(min_dists)

    GEN_UMAP(hparams)
    PLOT_UMAP(GEN_UMAP.out)

    png_data = PLOT_UMAP.out.collectFile(
        name: "png_data.txt", newLine: true) { it.toString() }
    SERVE_FLASK(png_data)
}
