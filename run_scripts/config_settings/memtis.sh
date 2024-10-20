CONFIG_PERF=off
CONFIG_NS=on
CONFIG_NW=off
CONFIG_CXL_MODE=off

function func_memtis_setting() {
    echo 10 | tee /proc/sys/vm/watermark_scale_factor

    echo 199 | tee /sys/kernel/mm/htmm/htmm_sample_period
    echo 100007 | tee /sys/kernel/mm/htmm/htmm_inst_sample_period
    echo 1 | tee /sys/kernel/mm/htmm/htmm_thres_hot
    echo 2 | tee /sys/kernel/mm/htmm/htmm_split_period

    # turn on hugepage
    # tune
    echo 100000 | tee /sys/kernel/mm/htmm/htmm_adaptation_period
    # tune
    echo 2000000 | tee /sys/kernel/mm/htmm/htmm_cooling_period
    echo 2 | tee /sys/kernel/mm/htmm/htmm_mode
    # tune
    echo 500 | tee /sys/kernel/mm/htmm/htmm_demotion_period_in_ms
    # tune
    echo 500 | tee /sys/kernel/mm/htmm/htmm_promotion_period_in_ms
    # tune
    echo 4 | tee /sys/kernel/mm/htmm/htmm_gamma
    ###  cpu cap (per mille) for ksampled
    # tune
    echo 30 | tee /sys/kernel/mm/htmm/ksampled_soft_cpu_quota

    if [[ "x${CONFIG_NS}" == "xoff" ]]; then
	echo 1 | tee /sys/kernel/mm/htmm/htmm_thres_split
    else
	echo 0 | tee /sys/kernel/mm/htmm/htmm_thres_split
    fi

    if [[ "x${CONFIG_NW}" == "xoff" ]]; then
	echo 0 | tee /sys/kernel/mm/htmm/htmm_nowarm
    else
	echo 1 | tee /sys/kernel/mm/htmm/htmm_nowarm
    fi

    if [[ "x${CONFIG_CXL_MODE}" == "xon" ]]; then
    # Not applicable in AMD
	# ${DIR}/scripts/set_uncore_freq.sh on
	echo "enabled" | tee /sys/kernel/mm/htmm/htmm_cxl_mode
    else
    # Not applicable in AMD
	# ${DIR}/scripts/set_uncore_freq.sh off
	echo "disabled" | tee /sys/kernel/mm/htmm/htmm_cxl_mode
    fi

    # echo "always" | tee /sys/kernel/mm/transparent_hugepage/enabled
    # echo "always" | tee /sys/kernel/mm/transparent_hugepage/defrag
}

echo 0 | sudo tee /proc/sys/kernel/numa_balancing
echo 0 | sudo tee /sys/kernel/mm/numa/demotion_enabled
func_memtis_setting
