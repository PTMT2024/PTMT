#!/bin/bash
echo 0 | sudo tee /proc/sys/kernel/numa_balancing
echo 0 | sudo tee /sys/kernel/mm/numa/demotion_enabled
echo 10 | sudo tee /proc/sys/vm/watermark_scale_factor
echo 15 | sudo tee /proc/sys/vm/zone_reclaim_mode
# echo 0 | sudo tee /proc/sys/vm/zone_reclaim_mode

# /home/sherry/projects/sk_prokect/mldpp/page_placement_tools/user_space_page_migration/user_space_page_migration -w 0 -q 0 &> ${LOG_DIR}/tune.log &
/home/sherry/projects/sk_prokect/mldpp/page_placement_tools/user_space_page_migration/user_space_page_migration -w 0 -q 0 &> /dev/null &