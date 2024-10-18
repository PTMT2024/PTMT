#!/bin/bash
#### default setting


echo 2 | sudo tee /proc/sys/kernel/numa_balancing
echo 1 | sudo tee /sys/kernel/mm/numa/demotion_enabled
echo 15 | sudo tee /proc/sys/vm/zone_reclaim_mode

# scan_size_mb is how many megabytes worth of pages are scanned for a given scan.
echo 256 | sudo tee /sys/kernel/debug/sched/numa_balancing/scan_size_mb

# scan_delay_ms is the starting “scan delay” used for a task when it initially forks.
echo 1000 | sudo tee /sys/kernel/debug/sched/numa_balancing/scan_delay_ms

# scan_period_max_ms is the maximum time in milliseconds to scan a tasks virtual memory. It effectively controls the minimum scanning rate for each task.
echo 60000 | sudo tee /sys/kernel/debug/sched/numa_balancing/scan_period_max_ms

# scan_period_min_ms is the minimum time in milliseconds to scan a tasks virtual memory. It effectively controls the maximum scanning rate for each task.
echo 1000 | sudo tee /sys/kernel/debug/sched/numa_balancing/scan_period_min_ms


echo 30 | sudo tee /proc/sys/kernel/numa_balancing_rate_limit_mbps
# echo 512 | sudo tee /proc/sys/kernel/numa_balancing_rate_limit_mbps

## enable early wakeup
echo 1 | sudo tee /proc/sys/kernel/numa_balancing_wake_up_kswapd_early

## enable decreasing hot threshold if the pages just demoted are hot
echo 1 | sudo tee /proc/sys/kernel/numa_balancing_scan_demoted

echo 16 | sudo tee /proc/sys/kernel/numa_balancing_demoted_threshold

echo 10 | sudo tee /proc/sys/kernel/numa_balancing_promote_watermark_mb

echo 1000 | sudo tee /proc/sys/kernel/numa_balancing_hot_threshold_ms

echo 1 | sudo tee /proc/sys/kernel/numa_balancing_mldpp
# echo 0 | sudo tee /proc/sys/kernel/numa_balancing_mldpp

echo 10 | sudo tee /proc/sys/vm/watermark_scale_factor
