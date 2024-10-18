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
BENCHMARKS="LU FT SP CG MG BT Graph500 BFS PageRank Liblinear Silo"
BENCHMARKS="PageRank_l BFS_l Silo_l"
BENCHMARKS="PageRank BFS Silo Graph500 Liblinear"
BENCHMARKS="PageRank-Twitter-Wrapper BFS-Twitter-Wrapper LU FT SP CG MG BT Graph500 BFS PageRank Liblinear Silo Silo_s Silo_x BFS_s BFS_x PageRank_x"
BENCHMARKS="PageRank-Twitter-Wrapper BFS-Twitter-Wrapper"
BENCHMARKS="PARSEC3-canneal PARSEC3-raytrace SPLASH2X-radix SPLASH2X-lu_ncb"
BENCHMARKS="PageRank"
BENCHMARKS="Silo_x BFS_x PageRank_x Graph500_s"
BENCHMARKS="FT_s SP_s BT_s LU_s"
BENCHMARKS="LU FT SP CG MG BT Graph500 BFS PageRank Liblinear Silo FT_s SP_s BT_s LU_s Silo_x BFS_x PageRank_x Graph500_s"
BENCHMARKS="FT_s SP_s BT_s LU_s Silo_x BFS_x PageRank_x Graph500_s"
BENCHMARKS="Graph500_s Liblinear_s"
BENCHMARKS="Graph500_s"


# MM="autonuma"
# MM="tiering08"
# MM="mldpp"
MM="tpp"
# MM="memtis"
LOCAL_DRAM_SIZE="34G"
# LOCAL_DRAM_SIZE="4G"

COLLECT_PERIOD=10
# COLLECT_PERIOD=30
# COLLECT_PERIOD=60

mkdir -p ./log

for BENCH in ${BENCHMARKS};
do
    export CURRENT_DATE=$(date +%Y%m%d%H%M)
	./scripts/run_bench.sh -T tune_rl_online -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
    sleep 15
done

# LEARNING_RATES="0 0.07"

# for LEARNING_RATE in ${LEARNING_RATES};
# do
#     export LEARNING_RATE
#     for BENCH in ${BENCHMARKS};
#     do
#         export CURRENT_DATE=$(date +%Y%m%d%H%M)
#     	./scripts/run_bench.sh -T tune_rl_online -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
#         sleep 15
#     done
# done


# DISCOUNT_FACTORS="0 0.2 0.5 0.9 0.99 1"

# for DISCOUNT_FACTOR in ${DISCOUNT_FACTORS};
# do
#     export DISCOUNT_FACTOR
#     for BENCH in ${BENCHMARKS};
#     do
#         export CURRENT_DATE=$(date +%Y%m%d%H%M)
#     	./scripts/run_bench.sh -T tune_rl_online -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
#         sleep 15
#     done
# done