#!/bin/bash

# BENCH_DIR=/mnt/nvme01/sherry/workloads/parsec-benchmark/bin
# BENCH_CMD="${BENCH_DIR}/parsecmgmt -a run -p streamcluster -i simlarge -n 1"

# # Mem size: 

# # BENCH_RUN="${BENCH_CMD}"

# APP_WRAPPER="python3 /home/sherry/projects/sk_prokect/mldpp/mldpp/app_wrapper.py"
# BENCH_RUN="${APP_WRAPPER} 24 ${BENCH_CMD}"

NTHREADS=1
BENCH_DIR=/mnt/nvme01/sherry/workloads/parsec-benchmark/pkgs/kernels
# Native size
BENCH_CMD="${BENCH_DIR}/streamcluster/inst/amd64-linux.gcc/bin/streamcluster 10 20 128 1000000 200000 5000 none output.txt ${NTHREADS}"
BENCH_RUN="${BENCH_CMD}"
