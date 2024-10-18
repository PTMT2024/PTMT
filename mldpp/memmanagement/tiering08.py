import subprocess
import importlib
import os
import subprocess
import datetime
import random
import csv
from utils import *
import datetime
from time import sleep
import sys
sys.path.append("..")


def reset_config_cmd(sys_config):
    subprocess.run([
        f'/home/sherry/projects/sk_prokect/mldpp/mldpp/memmanagement/scripts/tiering08/update.sh '
        f'{sys_config["numa_balancing_scan_size_mb"]} '
        f'{sys_config["numa_balancing_scan_period_min_ms"]} '
        f'{sys_config["numa_balancing_scan_period_max_ms"]} '
        f'{sys_config["numa_balancing_scan_delay_ms"]} '
        f'{sys_config["numa_balancing_promote_watermark_mb"]} '
        f'{sys_config["numa_balancing_rate_limit_mbps"]} '
        f'{sys_config["numa_balancing_hot_threshold_ms"]}'
    ], shell=True, text=True, check=True)

def update_config_cmd(sys_config):
    subprocess.run([
        f'/home/sherry/projects/sk_prokect/mldpp/mldpp/memmanagement/scripts/tiering08/update.sh '
        f'{sys_config["numa_balancing_scan_size_mb"]} '
        f'{sys_config["numa_balancing_scan_period_min_ms"]} '
        f'{sys_config["numa_balancing_scan_period_max_ms"]} '
        f'{sys_config["numa_balancing_scan_delay_ms"]} '
        f'{sys_config["numa_balancing_promote_watermark_mb"]} '
        f'{sys_config["numa_balancing_rate_limit_mbps"]} '
        f'{sys_config["numa_balancing_hot_threshold_ms"]}'
    ], shell=True, text=True, check=True)


def reset(bench_pid):
    sys_config = {
        "numa_balancing_scan_size_mb": 256,
        "numa_balancing_scan_period_min_ms": 1000,
        "numa_balancing_scan_period_max_ms": 60000,
        "numa_balancing_scan_delay_ms": 1000,
        "numa_balancing_promote_watermark_mb": 10,
        "numa_balancing_rate_limit_mbps": 30,
        "numa_balancing_hot_threshold_ms": 1000,
    }
    reset_config_cmd(sys_config)
    return sys_config

def reset_random(bench_pid):
    # numa_balancing_scan_size_mb = os.environ['numa_scan_size_mb']
    numa_balancing_scan_size_mb = 256
    numa_balancing_scan_period_min_ms = 1000
    numa_balancing_scan_period_max_ms = 60000 
    numa_balancing_scan_delay_ms = 1000
    # numa_balancing_promote_watermark_mb = random.choice([10, 64, 128 ,256, 512])
    # numa_balancing_promote_watermark_mb = random.choice([64 , 512])
    numa_balancing_promote_watermark_mb = os.environ.get("numa_balancing_promote_watermark_mb", 10)
    # numa_balancing_promote_watermark_mb = 10
    numa_balancing_rate_limit_mbps =   os.environ.get("promote_rate_limit", 30)
    numa_balancing_hot_threshold_ms = 1000

    sys_config = {
        "numa_balancing_scan_size_mb": numa_balancing_scan_size_mb,
        "numa_balancing_scan_period_min_ms": numa_balancing_scan_period_min_ms,
        "numa_balancing_scan_period_max_ms": numa_balancing_scan_period_max_ms,
        "numa_balancing_scan_delay_ms": numa_balancing_scan_delay_ms,
        "numa_balancing_promote_watermark_mb": numa_balancing_promote_watermark_mb,
        "numa_balancing_rate_limit_mbps": numa_balancing_rate_limit_mbps,
        "numa_balancing_hot_threshold_ms": numa_balancing_hot_threshold_ms,
    }
    reset_config_cmd(sys_config)
    return sys_config

def update_random(bench_pid):
    numa_balancing_scan_size_mb = random.choice([256, 1024, 4096, 8192])
    numa_balancing_scan_period_min_ms = 1000
    numa_balancing_scan_period_max_ms = 60000
    numa_balancing_scan_delay_ms = 1000
    numa_balancing_promote_watermark_mb = random.choice([10, 64, 128 ,256, 512])
    numa_balancing_rate_limit_mbps =  random.choice([30])
    # numa_balancing_hot_threshold_ms = random.choice([500, 1000, 2000])
    numa_balancing_hot_threshold_ms = 1000

    sys_config = {
        "numa_balancing_scan_size_mb": numa_balancing_scan_size_mb,
        "numa_balancing_scan_period_min_ms": numa_balancing_scan_period_min_ms,
        "numa_balancing_scan_period_max_ms": numa_balancing_scan_period_max_ms,
        "numa_balancing_scan_delay_ms": numa_balancing_scan_delay_ms,
        "numa_balancing_promote_watermark_mb": numa_balancing_promote_watermark_mb,
        "numa_balancing_rate_limit_mbps": numa_balancing_rate_limit_mbps,
        "numa_balancing_hot_threshold_ms": numa_balancing_hot_threshold_ms,
    }
    update_config_cmd(sys_config)
    return sys_config

def update_default(bench_pid):
    sys_config = {
        "numa_balancing_scan_size_mb": 256,
        "numa_balancing_scan_period_min_ms": 1000,
        "numa_balancing_scan_period_max_ms": 60000,
        "numa_balancing_scan_delay_ms": 1000,
        "numa_balancing_promote_watermark_mb": 10,
        "numa_balancing_rate_limit_mbps": 30,
        "numa_balancing_hot_threshold_ms": 1000,

    }
    update_config_cmd(sys_config)
    return sys_config

def update_default_with_ml(predictor, bench_pid, model_name, new_datapoint, target = 'latency'):
    min_latency_neighbor ,info = predictor.find_optimal_config(new_datapoint, target)
    numa_balancing_promote_watermark_mb = int(min_latency_neighbor['numa_balancing_promote_watermark_mb'])

    sys_config = {
        "numa_balancing_scan_size_mb": 256,
        "numa_balancing_scan_period_min_ms": 1000,
        "numa_balancing_scan_period_max_ms": 60000,
        "numa_balancing_scan_delay_ms": 1000,
        "numa_balancing_promote_watermark_mb": 10,
        "numa_balancing_rate_limit_mbps": 30,
        "numa_balancing_hot_threshold_ms": 1000,

    }
    update_config_cmd(sys_config)
    return sys_config
    
def update_ml(predictor, bench_pid, model_name, new_datapoint, target = 'latency'):
    min_latency_neighbor, info = predictor.find_optimal_config(new_datapoint, target)

    # numa_balancing_scan_size_mb = 256
    numa_balancing_scan_size_mb =  int(min_latency_neighbor['numa_balancing_scan_size_mb'])
    numa_balancing_scan_period_min_ms = 1000
    numa_balancing_scan_period_max_ms = 60000
    numa_balancing_scan_delay_ms = 1000
    numa_balancing_promote_watermark_mb = int(min_latency_neighbor['numa_balancing_promote_watermark_mb'])
    numa_balancing_rate_limit_mbps = 30
    # numa_balancing_hot_threshold_ms = int(min_latency_neighbor['numa_balancing_hot_threshold_ms'])
    numa_balancing_hot_threshold_ms = 1000


    sys_config = {
        "numa_balancing_scan_size_mb": numa_balancing_scan_size_mb,
        "numa_balancing_scan_period_min_ms": numa_balancing_scan_period_min_ms,
        "numa_balancing_scan_period_max_ms": numa_balancing_scan_period_max_ms,
        "numa_balancing_scan_delay_ms": numa_balancing_scan_delay_ms,
        "numa_balancing_promote_watermark_mb": numa_balancing_promote_watermark_mb,
        "numa_balancing_rate_limit_mbps": numa_balancing_rate_limit_mbps,
        "numa_balancing_hot_threshold_ms": numa_balancing_hot_threshold_ms,
    }
    update_config_cmd(sys_config)
    return sys_config, info

def update_rl(predicted_combination):
    numa_balancing_scan_size_mb =  int(predicted_combination['numa_balancing_scan_size_mb'])
    numa_balancing_scan_period_min_ms = 1000
    numa_balancing_scan_period_max_ms = 60000
    numa_balancing_scan_delay_ms = 1000
    numa_balancing_promote_watermark_mb = int(predicted_combination['numa_balancing_promote_watermark_mb'])
    numa_balancing_rate_limit_mbps = 30
    numa_balancing_hot_threshold_ms = 1000

    sys_config = {
        "numa_balancing_scan_size_mb": numa_balancing_scan_size_mb,
        "numa_balancing_scan_period_min_ms": numa_balancing_scan_period_min_ms,
        "numa_balancing_scan_period_max_ms": numa_balancing_scan_period_max_ms,
        "numa_balancing_scan_delay_ms": numa_balancing_scan_delay_ms,
        "numa_balancing_promote_watermark_mb": numa_balancing_promote_watermark_mb,
        "numa_balancing_rate_limit_mbps": numa_balancing_rate_limit_mbps,
        "numa_balancing_hot_threshold_ms": numa_balancing_hot_threshold_ms,
    }
    update_config_cmd(sys_config)
    return sys_config

def csv_headers():
    return [
        "ldram_size(MB)",
        "numa_balancing_scan_size_mb",
        "numa_balancing_promote_watermark_mb",
        "numa_balancing_rate_limit_mbps",
        "numa_balancing_hot_threshold_ms",
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
        sys_config["numa_balancing_scan_size_mb"],
        sys_config["numa_balancing_promote_watermark_mb"],
        sys_config["numa_balancing_rate_limit_mbps"],
        sys_config["numa_balancing_hot_threshold_ms"],
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
    ]
