#!/bin/bash

BENCH_DIR=/mnt/nvme01/sherry/workloads/gapbs
BENCH_CMD="${BENCH_DIR}/bfs -g 29 -n 300"

BENCH_RUN="${BENCH_CMD}"
# Mem footprint: 138GB