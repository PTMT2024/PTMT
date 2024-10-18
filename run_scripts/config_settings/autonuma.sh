#!/bin/bash

# valina kernel 6.1.0
echo 2 | sudo tee /proc/sys/kernel/numa_balancing
echo 1 | sudo tee /sys/kernel/mm/numa/demotion_enabled
echo 15 | sudo tee /proc/sys/vm/zone_reclaim_mode

# default configuration
# scan_size_mb is how many megabytes worth of pages are scanned for a given scan.
echo 256 | sudo tee /sys/kernel/debug/sched/numa_balancing/scan_size_mb

# scan_delay_ms is the starting “scan delay” used for a task when it initially forks.
echo 1000 | sudo tee /sys/kernel/debug/sched/numa_balancing/scan_delay_ms

# scan_period_max_ms is the maximum time in milliseconds to scan a tasks virtual memory. It effectively controls the minimum scanning rate for each task.
echo 60000 | sudo tee /sys/kernel/debug/sched/numa_balancing/scan_period_max_ms
# echo 400000 | sudo tee /sys/kernel/debug/sched/numa_balancing/scan_period_max_ms

# scan_period_min_ms is the minimum time in milliseconds to scan a tasks virtual memory. It effectively controls the maximum scanning rate for each task.
echo 1000 | sudo tee /sys/kernel/debug/sched/numa_balancing/scan_period_min_ms

echo 1000 | sudo tee /sys/kernel/debug/sched/numa_balancing/hot_threshold_ms

echo 65536 | sudo tee /proc/sys/kernel/numa_balancing_promote_rate_limit_MBps

echo 2560 | sudo tee /proc/sys/kernel/numa_balancing_max_scan_window
# echo 1 | sudo tee /proc/sys/kernel/numa_balancing_mldpp
echo 0 | sudo tee /proc/sys/kernel/numa_balancing_mldpp


# access latency = access timestamp - numascan timestamp 
# access latency < 1s

echo 10 | sudo tee /proc/sys/vm/watermark_scale_factor
