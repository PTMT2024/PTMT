#!/bin/bash

BENCH_DIR=/mnt/nvme01/sherry/workloads/parsec-benchmark/bin
BENCH_CMD="${BENCH_DIR}/parsecmgmt -a run -p fluidanimate -i native -n 1"

# Mem size: 

# BENCH_RUN="${BENCH_CMD}"

APP_WRAPPER="python3 /home/sherry/projects/sk_prokect/mldpp/mldpp/app_wrapper.py"
BENCH_RUN="${APP_WRAPPER} 24 ${BENCH_CMD}"