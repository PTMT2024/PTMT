#!/bin/bash

BENCH_DIR=/mnt/nvme01/sherry/workloads/graph500/omp-csr
BENCH_CMD="${BENCH_DIR}/omp-csr -s 26 -e 20 -V"

# Mem size: 46.4GGB
BENCH_RUN="${BENCH_CMD}"