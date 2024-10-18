#!/bin/bash

BENCHMARKS="XSBench PageRank Silo BTree"
BENCHMARKS="Graph500"
BENCHMARKS="FT SP MG BT"
BENCHMARKS="CG MG BFS PageRank Liblinear"
BENCHMARKS="Liblinear"
BENCHMARKS="PageRank"

# MM="autonuma"
# MM="tiering-0.8"
# MM="tpp"
# MM="memtis"
MM="mldpp"
LOCAL_DRAM_SIZE="34G"

COLLECT_PERIOD=10
# COLLECT_PERIOD=30
# COLLECT_PERIOD=60

mkdir -p ./log
for BENCH in ${BENCHMARKS};
do
    export CURRENT_DATE=$(date +%Y%m%d%H%M)
	./scripts/run_bench.sh -T defaulttunewithml -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
    sleep 15
done
