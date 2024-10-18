echo "numa_balancing_scan_size_mb: $1"
echo "numa_balancing_scan_period_min_ms: $2"
echo "numa_balancing_scan_period_max_ms: $3"
echo "numa_balancing_scan_delay_ms: $4"
echo "numa_balancing_promote_watermark_mb: $5"
echo "numa_balancing_rate_limit_mbps: $6"
echo "numa_balancing_hot_threshold_ms: $7"



echo $1 | sudo tee /sys/kernel/debug/sched/numa_balancing/scan_size_mb
echo $2 | sudo tee /sys/kernel/debug/sched/numa_balancing/scan_period_min_ms
echo $3 | sudo tee /sys/kernel/debug/sched/numa_balancing/scan_period_max_ms
echo $4 | sudo tee /sys/kernel/debug/sched/numa_balancing/scan_delay_ms
echo $5 | sudo tee /proc/sys/kernel/numa_balancing_promote_watermark_mb
echo $6 | sudo tee /proc/sys/kernel/numa_balancing_rate_limit_mbps
echo $7 | sudo tee /proc/sys/kernel/numa_balancing_hot_threshold_ms