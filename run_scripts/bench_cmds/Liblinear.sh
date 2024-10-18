#!/bin/bash

BENCH_DIR=/mnt/nvme01/sherry/workloads/liblinear-multicore-2.47
BENCH_CMD="${BENCH_DIR}/train -s 6 -m 24 ${BENCH_DIR}/datasets/kdd12"

# Mem size: 69GB 
BENCH_RUN="${BENCH_CMD}"