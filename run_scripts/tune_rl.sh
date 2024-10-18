#!/bin/bash

BENCHMARKS="XSBench PageRank Silo BTree"
BENCHMARKS="Graph500"
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
BENCHMARKS="Graph500"
BENCHMARKS="LU LU FT FT SP SP CG CG MG MG BT BT Graph500 Graph500 BFS BFS PageRank PageRank Liblinear Liblinear Silo Silo"
BENCHMARKS="PageRank_l BFS_l Silo_l Silo_s Silo_x"
BENCHMARKS="Graph500_s"


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
	./scripts/run_bench.sh -T tune_rl -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
    sleep 15
done
