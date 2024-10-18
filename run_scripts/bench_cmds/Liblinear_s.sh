#!/bin/bash

BENCH_DIR=/mnt/nvme01/sherry/workloads/liblinear-multicore-2.47
BENCH_CMD="${BENCH_DIR}/train -s 6 -m 24 ${BENCH_DIR}/datasets/criteo.kaggle2014.svm/train.txt.svm"

# Mem size: 
BENCH_RUN="${BENCH_CMD}"