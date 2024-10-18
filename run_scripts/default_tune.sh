#!/bin/bash

BENCHMARKS="Graph500"
BENCHMARKS="FT SP MG BT"
BENCHMARKS="LU CG Liblinear Graph500"
BENCHMARKS="MG FT BT"
BENCHMARKS="CG LU SP Graph500 BFS PageRank Liblinear"
BENCHMARKS="PageRank Liblinear"
BENCHMARKS="Liblinear"
BENCHMARKS="FT"
BENCHMARKS="LU FT SP CG MG BT Graph500 BFS PageRank Liblinear"
BENCHMARKS="LU SP CG MG BT Graph500 BFS PageRank Liblinear"
BENCHMARKS="BFS PageRank"

# MM="tiering08"
# MM="tpp"
# MM="memtis"
# MM="mldpp"
MM="autonuma"
LOCAL_DRAM_SIZE="34G"
# COLLECT_PERIOD=10
COLLECT_PERIOD=30
# COLLECT_PERIOD=60

mkdir -p ./log
for BENCH in ${BENCHMARKS};
do
    export CURRENT_DATE=$(date +%Y%m%d%H%M)
	./scripts/run_bench.sh -T defaulttune -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
    sleep 15
done
