#!/bin/bash

BENCHMARKS="Graph500"
BENCHMARKS="FT SP MG BT"
BENCHMARKS="LU CG Liblinear Graph500"
BENCHMARKS="MG FT BT"
BENCHMARKS="CG LU SP Graph500 BFS PageRank Liblinear"
BENCHMARKS="PageRank Liblinear"
BENCHMARKS="Liblinear"
BENCHMARKS="FT"
BENCHMARKS="LU FT SP CG MG BT Graph500 BFS PageRank Liblinear Silo"
BENCHMARKS="LU SP CG MG BT Graph500 BFS PageRank Liblinear"
BENCHMARKS="PageRank_l BFS_l Silo_l"
BENCHMARKS="PageRank_x BFS_x BFS_s"
BENCHMARKS="PageRank_x BFS_x"
# BENCHMARKS="PARSEC3-canneal PARSEC3-fluidanimate PARSEC3-streamcluster PARSEC3-x264 SPLASH-raytrace SPLASH-water_nsquared SPLASH2X-barnes SPLASH2X-lu_ncb SPLASH2X-ocean_ncp"
BENCHMARKS="PageRank-Twitter BFS-Twitter"
BENCHMARKS="PageRank-Twitter-Wrapper BFS-Twitter-Wrapper"
BENCHMARKS="PARSEC3-canneal PARSEC3-raytrace SPLASH2X-radix SPLASH2X-lu_ncb"
BENCHMARKS="PageRank"
BENCHMARKS="Silo_x BFS_x PageRank_x Graph500_s"
BENCHMARKS="PageRank_x "
BENCHMARKS="LU FT SP CG MG BT Graph500 BFS PageRank Liblinear Silo FT_s SP_s BT_s LU_s Silo_x BFS_x PageRank_x Graph500_s"
BENCHMARKS="FT_s SP_s BT_s LU_s Silo_x BFS_x PageRank_x Graph500_s"
BENCHMARKS="LU FT SP CG MG BT Graph500 BFS PageRank Liblinear Silo"
BENCHMARKS="Graph500"
BENCHMARKS="LU FT SP CG MG BT BFS PageRank Liblinear Graph500 Silo FT_s SP_s BT_s LU_s Silo_x Graph500_s Liblinear_s"
BENCHMARKS="CG"

# MM="tiering08"
# MM="tpp"
# MM="memtis"
# MM="mldpp"
MM="autonuma"
LOCAL_DRAM_SIZE="34G"
# LOCAL_DRAM_SIZE="4G"
COLLECT_PERIOD=10
# COLLECT_PERIOD=30
# COLLECT_PERIOD=60

mkdir -p ./log
for BENCH in ${BENCHMARKS};
do
    export CURRENT_DATE=$(date +%Y%m%d%H%M)
	./scripts/run_bench.sh -T onedefaulttune -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
    sleep 15
done
