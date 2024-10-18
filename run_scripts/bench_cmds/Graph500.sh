#!/bin/bash

BENCH_DIR=/mnt/nvme01/sherry/workloads/graph500/omp-csr
BENCH_CMD="${BENCH_DIR}/omp-csr -s 27 -e 15 -V"

# Mem size: 64GB
BENCH_RUN="${BENCH_CMD}"