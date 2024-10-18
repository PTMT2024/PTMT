#!/bin/bash

BENCH_DIR=/mnt/nvme01/sherry/workloads/silo/out-perf.masstree/benchmarks
BENCH_CMD="${BENCH_DIR}/dbtest --verbose --bench ycsb --num-threads 20 --scale-factor 1000000 --ops-per-worker=200000000"

# Mem size: 148247MB
BENCH_RUN="${BENCH_CMD}"