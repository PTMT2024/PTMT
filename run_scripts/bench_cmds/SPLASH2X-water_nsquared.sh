#!/bin/bash

BENCH_DIR=/mnt/nvme01/sherry/workloads/parsec-benchmark/bin
BENCH_CMD="${BENCH_DIR}/parsecmgmt -a run -p splash2x.water_nsquared -i native -n 1"

# Mem size: 
# BENCH_RUN="${BENCH_CMD}"

APP_WRAPPER="python3 /home/sherry/projects/sk_prokect/mldpp/mldpp/app_wrapper.py"
BENCH_RUN="${APP_WRAPPER} 24 ${BENCH_CMD}"

# /mnt/nvme01/sherry/workloads/parsec-benchmark/ext/splash2x/apps/water_nsquared/inst/amd64-linux.gcc/bin/run.sh: 1: eval: cannot open input_1: No such file