import subprocess
import importlib
import os
import subprocess
import random
import csv
from utils import *
import datetime
from time import sleep
import sys
sys.path.append("..")

def reset_config_cmd(sys_config):
    subprocess.run([
        f'/home/sherry/projects/sk_prokect/mldpp/mldpp/memmanagement/scripts/autonuma/reset.sh '
        f'{sys_config["numa_balancing_hot_threshold_ms"]} '
        f'{sys_config["numa_balancing_promote_rate_limit_MBps"]} '
        f'{sys_config["numa_balancing_scan_period_min_ms"]} '
        f'{sys_config["numa_balancing_max_scan_window"]} '
        f'{sys_config["numa_scan_size_mb"]} '
        f'{sys_config["watermark_scale_factor"]} '
        f'{sys_config["numa_balancing_scan_period_max_ms"]} '
        f'{sys_config["scan_delay_ms"]} '
    ], shell=True, text=True, check=True)

def update_config_cmd(sys_config):
    subprocess.run([
        f'/home/sherry/projects/sk_prokect/mldpp/mldpp/memmanagement/scripts/autonuma/update.sh '
        f'{sys_config["numa_balancing_hot_threshold_ms"]} '
        f'{sys_config["numa_balancing_promote_rate_limit_MBps"]} '
        f'{sys_config["numa_balancing_scan_period_min_ms"]} '
        f'{sys_config["numa_balancing_max_scan_window"]} '
        f'{sys_config["numa_scan_size_mb"]} '
        f'{sys_config["watermark_scale_factor"]} '
    ], shell=True, text=True, check=True)

def default_config(bench_pid):
    sys_config = {
        "numa_balancing_hot_threshold_ms": 1000,
        "numa_balancing_promote_rate_limit_MBps": 65536,
        "numa_balancing_scan_period_min_ms": 1000,
        "numa_balancing_max_scan_window": 2560,
        "numa_scan_size_mb": 256,
        "watermark_scale_factor": 10,
    }
    return sys_config

def reset(bench_pid):
    sys_config = {
        "numa_balancing_hot_threshold_ms": 1000,
        "numa_balancing_promote_rate_limit_MBps": 65536,
        "numa_balancing_scan_period_min_ms": 1000,
        "numa_balancing_max_scan_window": 2560,
        "numa_scan_size_mb": 256,
        "watermark_scale_factor": 10,
        "numa_balancing_scan_period_max_ms": 60000,
        "scan_delay_ms": 1000,
    }
    reset_config_cmd(sys_config)
    return sys_config

def reset_random(bench_pid):
    sys_config = {
        "numa_balancing_hot_threshold_ms": 1000,
        "numa_balancing_promote_rate_limit_MBps": 65536,
        # "numa_balancing_scan_period_min_ms": random.choice([500, 1000, 10000]),
        "numa_balancing_scan_period_min_ms": os.environ.get("numa_balancing_scan_period_min_ms", 1000),
        # "numa_balancing_max_scan_window": random.choice([25600]),
        # "numa_balancing_max_scan_window": random.choice([640, 1280, 2560, 5120, 10240]),
        "numa_balancing_max_scan_window": 2560,
        # "numa_scan_size_mb": random.choice([256, 512, 1024, 2048, 4096, 8192]),
        # "numa_scan_size_mb": random.choice([256, 1024, 4096, 8192]),
        # "numa_scan_size_mb": random.choice([8192]),
        "numa_scan_size_mb": os.environ.get("numa_scan_size_mb", 256),
        "watermark_scale_factor": os.environ.get("watermark_scale_factor", 10),
        "numa_balancing_scan_period_max_ms": os.environ.get("numa_balancing_scan_period_max_ms", 60000),
        "scan_delay_ms": os.environ.get("scan_delay_ms", 1000),
    }
    print("reset_random sys_config: ", sys_config)
    reset_config_cmd(sys_config)
    return sys_config

def update_random(bench_pid):
    sys_config = {
        # "numa_balancing_hot_threshold_ms": random.choice([250, 500, 1000, 2000, 4000]),
        "numa_balancing_hot_threshold_ms": 1000,
        "numa_balancing_promote_rate_limit_MBps": 65536,
        "numa_balancing_scan_period_min_ms": 1000,
        "numa_balancing_max_scan_window": 2560,
        "numa_scan_size_mb": random.choice([256, 1024, 4096, 8192]),
        # "watermark_scale_factor": random.choice([5, 10, 50, 100]),
        "watermark_scale_factor": 10,
    }
    update_config_cmd(sys_config)
    return sys_config

def update_default(bench_pid):
    sys_config = {
        "numa_balancing_hot_threshold_ms": 1000,
        "numa_balancing_promote_rate_limit_MBps": 65536,
        "numa_balancing_scan_period_min_ms": 1000,
        "numa_balancing_max_scan_window": 2560,
        "numa_scan_size_mb": 256,
        "watermark_scale_factor": 10,
    }
    update_config_cmd(sys_config)
    return sys_config

def update_default_with_ml(predictor, bench_pid, model_name, new_datapoint, target = 'latency'):
    min_latency_neighbor ,info = predictor.find_optimal_config(new_datapoint, target)

    numa_balancing_hot_threshold_ms = int(min_latency_neighbor['numa_balancing_hot_threshold_ms'])

    sys_config = {
        "numa_balancing_hot_threshold_ms": 1000,
        "numa_balancing_promote_rate_limit_MBps": 65536,
        "numa_balancing_scan_period_min_ms": 1000,
        "numa_balancing_max_scan_window": 2560,
        "numa_scan_size_mb": 256,
        "watermark_scale_factor": 10,
    }
    update_config_cmd(sys_config)
    return sys_config
    
def update_ml(predictor, bench_pid, model_name, new_datapoint, target = 'latency'):
    min_latency_neighbor, info = predictor.find_optimal_config(new_datapoint, target)

    numa_balancing_hot_threshold_ms = int(min_latency_neighbor['numa_balancing_hot_threshold_ms'])
    numa_balancing_promote_rate_limit_MBps = int(min_latency_neighbor['numa_balancing_promote_rate_limit_MBps'])
    numa_balancing_scan_period_min_ms = int(min_latency_neighbor['numa_balancing_scan_period_min_ms'])
    numa_balancing_max_scan_window = int(min_latency_neighbor['numa_balancing_max_scan_window'])
    numa_scan_size_mb =  int(min_latency_neighbor['numa_scan_size_mb'])
    watermark_scale_factor = int(min_latency_neighbor['watermark_scale_factor'])

    sys_config = {
        "numa_balancing_hot_threshold_ms": numa_balancing_hot_threshold_ms,
        "numa_balancing_promote_rate_limit_MBps": numa_balancing_promote_rate_limit_MBps,
        "numa_balancing_scan_period_min_ms": numa_balancing_scan_period_min_ms,
        "numa_balancing_max_scan_window": numa_balancing_max_scan_window,
        "numa_scan_size_mb": numa_scan_size_mb,
        "watermark_scale_factor": watermark_scale_factor,
    }
    update_config_cmd(sys_config)
    return sys_config, info

def update_rl(predicted_combination):
    numa_balancing_hot_threshold_ms =  1000
    numa_balancing_promote_rate_limit_MBps =  65536
    numa_balancing_scan_period_min_ms =  1000
    numa_balancing_max_scan_window = 2560
    watermark_scale_factor = 10
    numa_scan_size_mb =  int(predicted_combination['numa_scan_size_mb'])

    sys_config = {
        "numa_balancing_hot_threshold_ms": numa_balancing_hot_threshold_ms,
        "numa_balancing_promote_rate_limit_MBps": numa_balancing_promote_rate_limit_MBps,
        "numa_balancing_scan_period_min_ms": numa_balancing_scan_period_min_ms,
        "numa_balancing_max_scan_window": numa_balancing_max_scan_window,
        "numa_scan_size_mb": numa_scan_size_mb,
        "watermark_scale_factor": watermark_scale_factor,
    }
    update_config_cmd(sys_config)
    return sys_config

def csv_headers():
    return [
        "ldram_size(MB)",
        "numa_balancing_hot_threshold_ms",
        "numa_balancing_promote_rate_limit_MBps",
        "numa_balancing_scan_period_min_ms",
        "numa_balancing_max_scan_window",
        "numa_scan_size_mb",
        "watermark_scale_factor",
        "instructions",
        "cycles",
        "ipc",
        "ipus",
        "written_to_pmm(MB/s)",
        "read_from_pmm(MB/s)",
        "written_to_dram(MB/s)",
        "read_from_dram(MB/s)",
        "l3cache_misses(/us)",
        "l2cache_misses(/us)",
        "l3cache_hit_ratio",
        "l2cache_hit_ratio",
        "llc_read_miss_latency(ns)",
        "exec_time(s)",
        "workload_runtime(s)",
    ]


def csv_values(ldram_size, sys_config, metrics_result, workload_result):
    return [
        ldram_size,
        sys_config["numa_balancing_hot_threshold_ms"],
        sys_config["numa_balancing_promote_rate_limit_MBps"],
        sys_config["numa_balancing_scan_period_min_ms"],
        sys_config["numa_balancing_max_scan_window"],
        sys_config["numa_scan_size_mb"],
        sys_config["watermark_scale_factor"],
        metrics_result["Instructions"],
        metrics_result["Cycles"],
        metrics_result["IPC"],
        metrics_result["IPUS"],
        metrics_result["WrittenToPMM"],
        metrics_result["ReadFromPMM"],
        metrics_result["WrittenToDRAM"],
        metrics_result["ReadFromDRAM"],
        metrics_result["L3CacheMisses"],
        metrics_result["L2CacheMisses"],
        metrics_result["L3CacheHitRatio"],
        metrics_result["L2CacheHitRatio"],
        metrics_result["LLCReadMissLatency"],
        metrics_result["ExecutionTime"],
        # workload_result["ExecutionTime"],
    ]
