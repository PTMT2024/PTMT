echo "memtis_htmm_thres_hot: $1"
echo "memtis_htmm_adaptation_period: $2"
echo "memtis_htmm_demotion_period_in_ms: $3"
echo "memtis_htmm_promotion_period_in_ms: $4"
echo "memtis_htmm_cooling_period: $5"
echo "memtis_htmm_gamma: $6"
echo "memtis_htmm_ksampled_soft_cpu_quota: $7"

echo $1 | sudo tee /sys/kernel/mm/htmm/htmm_thres_hot
echo $2 | sudo tee /sys/kernel/mm/htmm/htmm_adaptation_period
echo $3 | sudo tee /sys/kernel/mm/htmm/htmm_demotion_period_in_ms
echo $4 | sudo tee /sys/kernel/mm/htmm/htmm_promotion_period_in_ms
echo $5 | sudo tee /sys/kernel/mm/htmm/htmm_cooling_period
echo $6 | sudo tee /sys/kernel/mm/htmm/htmm_gamma
echo $7 | sudo tee /sys/kernel/mm/htmm/ksampled_soft_cpu_quota