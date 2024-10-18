#!/bin/bash

BENCH_DIR=/home/jieliu/sherrywang/pagemigration/workloads/BTree/BENCH_DIR
BENCH_CMD="${BENCH_DIR}/bench_btree_mt -- -n 2147483648  -l 10000000000"

# Mem size: 128GB
BENCH_RUN="${BENCH_CMD}"