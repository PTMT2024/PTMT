#!/bin/bash

BENCH_DIR=/mnt/nvme01/sherry/workloads/gapbs
BENCH_CMD="${BENCH_DIR}/pr -g 29 -n 8"
# Mem footprint: 132GB
BENCH_RUN="${BENCH_CMD}"