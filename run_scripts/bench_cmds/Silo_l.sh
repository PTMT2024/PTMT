#!/bin/bash

BENCH_DIR=/mnt/nvme01/sherry/workloads/silo/out-perf.masstree/benchmarks
BENCH_CMD="${BENCH_DIR}/dbtest --verbose --bench ycsb --num-threads 20 --scale-factor 800000 --ops-per-worker=600000000"

# Mem size: 115.8GB
BENCH_RUN="${BENCH_CMD}"