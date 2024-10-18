#!/bin/bash
echo 0 | sudo tee /proc/sys/kernel/numa_balancing
echo 0 | sudo tee /sys/kernel/mm/numa/demotion_enabled
echo 10 | sudo tee /proc/sys/vm/watermark_scale_factor
echo 256 | sudo tee /sys/kernel/debug/sched/numa_balancing/scan_size_mb