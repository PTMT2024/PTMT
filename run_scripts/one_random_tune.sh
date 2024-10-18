#!/bin/bash

BENCHMARKS="XSBench PageRank Silo BTree"
BENCHMARKS="FT"
BENCHMARKS="Graph500 FT SP MG BT"
BENCHMARKS="SP"
BENCHMARKS="FT"
BENCHMARKS="Silo"
BENCHMARKS="LU FT SP CG MG BT Graph500 BFS PageRank Liblinear Silo"
BENCHMARKS="Graph500 BFS PageRank Liblinear Silo"
BENCHMARKS="Graph500 CG"
BENCHMARKS="Graph500_s BT_s LU_s"
BENCHMARKS="Graph500_s LU_s SP_s Silo_x CG Graph500"
BENCHMARKS="Graph500"

# MM="autonuma"
MM="tiering08"
# MM="tpp"
# MM="memtis"
# MM="mldpp"
LOCAL_DRAM_SIZE="34G"

COLLECT_PERIOD=10
# COLLECT_PERIOD=30
# COLLECT_PERIOD=60

demote_scale_factors="100 200 400 800"
hotpage_thresholds="1 8 10"
hotpage_thresholds="1"
numa_scan_size_mbs="256 1024 4096 8192"
numa_scan_size_mbs="256"

mkdir -p ./log

# # UPM
# for hotpage_threshold in ${hotpage_thresholds};
# do
#     export hotpage_threshold
#     for BENCH in ${BENCHMARKS};
#     do
#         export CURRENT_DATE=$(date +%Y%m%d%H%M)
#     	./scripts/run_bench.sh -T onerandomtune -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
#         sleep 15
#     done
# done

# # TPP
# for demote_scale_factor in ${demote_scale_factors};
# do
#     export demote_scale_factor
#     for BENCH in ${BENCHMARKS};
#     do
#         export CURRENT_DATE=$(date +%Y%m%d%H%M)
#     	./scripts/run_bench.sh -T onerandomtune -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
#         sleep 15
#     done
# done

# # AutoNUMA
# numa_scan_size_mbs="64 1024"
# for numa_scan_size_mb in ${numa_scan_size_mbs};
# do
#     export numa_scan_size_mb
#     for BENCH in ${BENCHMARKS};
#     do
#         export CURRENT_DATE=$(date +%Y%m%d%H%M)
#     	./scripts/run_bench.sh -T onerandomtune -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
#         sleep 15
#     done
#     unset numa_scan_size_mb
# done

# scan_delay_mss="256 4000"
# for scan_delay_ms in ${scan_delay_mss};
# do
#     export scan_delay_ms
#     for BENCH in ${BENCHMARKS};
#     do
#         export CURRENT_DATE=$(date +%Y%m%d%H%M)
#     	./scripts/run_bench.sh -T onerandomtune -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
#         sleep 15
#     done
#     unset scan_delay_ms
# done

# numa_balancing_scan_period_min_mss="256 4000"
# for numa_balancing_scan_period_min_ms in ${numa_balancing_scan_period_min_mss};
# do
#     export numa_balancing_scan_period_min_ms
#     for BENCH in ${BENCHMARKS};
#     do
#         export CURRENT_DATE=$(date +%Y%m%d%H%M)
#     	./scripts/run_bench.sh -T onerandomtune -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
#         sleep 15
#     done
#     unset numa_balancing_scan_period_min_ms
# done

# numa_balancing_scan_period_max_mss="15000 240000"
# for numa_balancing_scan_period_max_ms in ${numa_balancing_scan_period_max_mss};
# do
#     export numa_balancing_scan_period_max_ms
#     for BENCH in ${BENCHMARKS};
#     do
#         export CURRENT_DATE=$(date +%Y%m%d%H%M)
#     	./scripts/run_bench.sh -T onerandomtune -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
#         sleep 15
#     done
#     unset numa_balancing_scan_period_max_ms
# done

# watermark_scale_factors="2 40"
# for watermark_scale_factor in ${watermark_scale_factors};
# do
#     export watermark_scale_factor
#     for BENCH in ${BENCHMARKS};
#     do
#         export CURRENT_DATE=$(date +%Y%m%d%H%M)
#     	./scripts/run_bench.sh -T onerandomtune -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
#         sleep 15
#     done
#     unset watermark_scale_factor
# done

# Tiering08
# numa_balancing_promote_watermark_mbs="10 64 128 256 512"
numa_balancing_promote_watermark_mbs="2 10"
numa_balancing_promote_watermark_mbs="64"
for numa_balancing_promote_watermark_mb in ${numa_balancing_promote_watermark_mbs};
do
    export numa_balancing_promote_watermark_mb
    for BENCH in ${BENCHMARKS};
    do
        export CURRENT_DATE=$(date +%Y%m%d%H%M)
    	./scripts/run_bench.sh -T onerandomtune -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
        sleep 15
    done
    unset numa_balancing_promote_watermark_mb
done

# promote_rate_limits="8 120"
# for promote_rate_limit in ${promote_rate_limits};
# do
#     export promote_rate_limit
#     for BENCH in ${BENCHMARKS};
#     do
#         export CURRENT_DATE=$(date +%Y%m%d%H%M)
#     	./scripts/run_bench.sh -T onerandomtune -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
#         sleep 15
#     done
#     unset promote_rate_limit
# done

# Tiering08
# for numa_scan_size_mb in ${numa_scan_size_mbs};
# do
#     export numa_scan_size_mb
#     for BENCH in ${BENCHMARKS};
#     do
#         export CURRENT_DATE=$(date +%Y%m%d%H%M)
#     	./scripts/run_bench.sh -T onerandomtune -B ${BENCH} -MM ${MM} -LM ${LOCAL_DRAM_SIZE} -CP ${COLLECT_PERIOD}
#         sleep 15
#     done
# done