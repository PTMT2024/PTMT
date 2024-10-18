#!/bin/bash

BENCH_DIR=/mnt/nvme01/sherry/workloads/XSBench/openmp-threading
BENCH_CMD="${BENCH_DIR}/XSBench -t 24 -s XL -p 15000000"

# Mem size: 116.5G 

# BENCH_CMD="${BENCH_DIR}/XSBench -t 24 -g 260000 -p 30000000"
# Mem size: 63.4GB 

BENCH_RUN="${BENCH_CMD}"