#!/bin/bash

BENCHMARKS="XSBench PageRank Silo BTree"
BENCHMARKS="Liblinear"
BENCHMARKS="CG MG"
# BENCHMARKS="SP"
# BENCHMARKS="PageRank Liblinear FT SP BT MG"
# BENCHMARKS="FT SP BT"
BENCHMARKS="BFS LU"
BENCHMARKS="PageRank"
BENCHMARKS="LU SP CG MG BT Graph500 BFS"
BENCHMARKS="PageRank"
BENCHMARKS="Liblinear FT"
BENCHMARKS="LU FT SP CG MG BT Graph500 BFS PageRank Liblinear"
BENCHMARKS="LU FT SP CG MG BT Graph500 BFS PageRank Liblinear Silo"
BENCHMARKS="Silo"

# MM="autonuma"
# MM="tiering08"
# MM="mldpp"
MM="tpp"
# MM="memtis"
LOCAL_DRAM_SIZE="34G"

COLLECT_PERIOD=10
# COLLECT_PERIOD=30
# COLLECT_PERIOD=60

mkdir -p ./log
for BENCH in ${BENCHMARKS};
do
    export CURRENT_DATE=$(date +%Y%m%d%H%M)
	./scripts/run_bench.sh -T tune_dnn -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
    sleep 15
done
