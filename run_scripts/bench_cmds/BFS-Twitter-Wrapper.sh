#!/bin/bash

BENCH_DIR=/mnt/nvme01/sherry/workloads/gapbs
GRAPH_DIR=/mnt/nvme01/sherry/workloads/gapbs/benchmark/graphs
# BENCH_CMD="${BENCH_DIR}/bfs -f ${GRAPH_DIR}/twitter.sg -n256"
BENCH_CMD="${BENCH_DIR}/bfs -f ${GRAPH_DIR}/twitter.sg -n64"

APP_WRAPPER="python3 /home/sherry/projects/sk_prokect/mldpp/mldpp/app_wrapper.py"
BENCH_RUN="${APP_WRAPPER} 8 ${BENCH_CMD}"

