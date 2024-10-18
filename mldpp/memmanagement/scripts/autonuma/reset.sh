echo "numa_balancing_hot_threshold_ms: $1"
echo "numa_balancing_promote_rate_limit_MBps: $2"
echo "numa_balancing_scan_period_min_ms: $3"
echo "numa_scan_size_mb: $5"
echo "watermark_scale_factor $6"
echo "numa_balancing_scan_period_max_ms: $7"
echo "numa_balancing_scan_delay_ms: $8"

echo $1 | sudo tee /sys/kernel/debug/sched/numa_balancing/hot_threshold_ms
echo $2 | sudo tee /proc/sys/kernel/numa_balancing_promote_rate_limit_MBps
echo $3 | sudo tee /sys/kernel/debug/sched/numa_balancing/scan_period_min_ms
echo $5 | sudo tee /sys/kernel/debug/sched/numa_balancing/scan_size_mb
echo $6 | sudo tee /proc/sys/vm/watermark_scale_factor
echo $7 | sudo tee /sys/kernel/debug/sched/numa_balancing/scan_period_max_ms
echo $8 | sudo tee /sys/kernel/debug/sched/numa_balancing/scan_delay_ms
