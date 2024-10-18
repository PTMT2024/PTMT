#!/bin/bash

BENCH_DIR=/mnt/nvme01/sherry/workloads/gapbs

BENCH_CMD="${BENCH_DIR}/pr -g 28 -n 48"
# Mem footprint: 70.1G
BENCH_RUN="${BENCH_CMD}"