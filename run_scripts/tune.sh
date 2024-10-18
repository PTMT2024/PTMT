#!/bin/bash

BENCHMARKS="XSBench PageRank Silo BTree"
BENCHMARKS="Graph500"
BENCHMARKS="Liblinear"
BENCHMARKS="CG MG"
BENCHMARKS="Graph500"
BENCHMARKS="BFS LU"
BENCHMARKS="PageRank"
BENCHMARKS="LU FT SP CG MG BT Graph500 BFS PageRank Liblinear"
BENCHMARKS="LU SP CG MG BT Graph500 BFS"
BENCHMARKS="Liblinear FT"

MM="autonuma"
# MM="tiering08"
# MM="memtis"
# MM="mldpp"
# MM="tpp"
LOCAL_DRAM_SIZE="34G"

COLLECT_PERIOD=30
# COLLECT_PERIOD=30
# COLLECT_PERIOD=60

mkdir -p ./log
for BENCH in ${BENCHMARKS};
do
    export CURRENT_DATE=$(date +%Y%m%d%H%M)
	./scripts/run_bench.sh -T tune -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
    sleep 15
done
