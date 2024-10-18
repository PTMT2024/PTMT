#!/bin/bash

BENCHMARKS="XSBench PageRank Silo BTree"
BENCHMARKS="FT"
BENCHMARKS="Graph500"
# BENCHMARKS="LU FT SP CG MG BT Graph500"
BENCHMARKS="Liblinear PageRank BFS"
BENCHMARKS="PageRank"
# BENCHMARKS="CG"
BENCHMARKS="LU FT SP CG MG BT Graph500 BFS PageRank Liblinear"
BENCHMARKS="LU FT SP CG MG BT Graph500 BFS PageRank Liblinear"
# BENCHMARKS="PageRank-Twitter-Wrapper BFS-Twitter-Wrapper"
BENCHMARKS="PARSEC3-fluidanimate PARSEC3-streamcluster PARSEC3-x264 SPLASH2X-raytrace"
BENCHMARKS="PARSEC3-canneal PARSEC3-raytrace SPLASH2X-radix SPLASH2X-lu_ncb"

MM="notune"
LOCAL_DRAM_SIZE="34G"
LOCAL_DRAM_SIZE="4G"

COLLECT_PERIOD=10
# COLLECT_PERIOD=30
# COLLECT_PERIOD=60

mkdir -p ./log
for BENCH in ${BENCHMARKS};
do
    export CURRENT_DATE=$(date +%Y%m%d%H%M)
	./scripts/run_bench.sh -T notune -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
    sleep 15
done
