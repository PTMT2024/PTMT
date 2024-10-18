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
BENCHMARKS="CG FT PageRank Graph500 Silo"
BENCHMARKS="SP"
BENCHMARKS="PageRank_l BFS_l Silo_l Silo_s Silo_x"
BENCHMARKS="gups-random"
BENCHMARKS="gups-hotset-move"
BENCHMARKS="LU FT SP CG MG BT Graph500 BFS PageRank Liblinear Silo"
BENCHMARKS="Silo"
BENCHMARKS="LU FT SP CG MG BT Graph500 BFS PageRank Liblinear Silo"
BENCHMARKS="SP CG MG BT"
BENCHMARKS="PageRank"
BENCHMARKS="Silo_x BFS_x PageRank_x Graph500_s"
BENCHMARKS="FT_s SP_s BT_s LU_s"
BENCHMARKS="LU FT SP CG MG BT Graph500 BFS PageRank Liblinear Silo FT_s SP_s BT_s LU_s Silo_x BFS_x PageRank_x Graph500_s"
BENCHMARKS="FT_s SP_s BT_s LU_s Silo_x Graph500_s Liblinear_s"
BENCHMARKS="Graph500_s"

# MM="autonuma"
# MM="tiering08"
# MM="mldpp"
MM="tpp"
# MM="memtis"
LOCAL_DRAM_SIZE="34G"

# COLLECT_PERIOD=10
# COLLECT_PERIOD=30
COLLECT_PERIOD=2
# COLLECT_PERIOD=60


# HOTSETS="37"
# HOTSETS="30 31 32 33 34 37"
mkdir -p ./log
for BENCH in ${BENCHMARKS};
do
    # for HOTSET in ${HOTSETS};
    # do
    export HOTSET
    export CURRENT_DATE=$(date +%Y%m%d%H%M)
	./scripts/run_bench.sh -T idt_tune -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
    sleep 15
    # done
done
