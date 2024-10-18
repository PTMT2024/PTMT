#!/bin/bash

BENCH_DIR=/mnt/nvme01/sherry/workloads/GUPS
BENCH_CMD="${BENCH_DIR}/gups 24 1000000000 37 8 ${HOTSET}"

# Mem size:
BENCH_RUN="${BENCH_CMD}"