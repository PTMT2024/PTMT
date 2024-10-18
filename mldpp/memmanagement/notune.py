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

def reset(bench_pid):
    sys_config = {
        "numa_balancing_scan_size_mb": 256,
        "numa_balancing_scan_period_min_ms": 1000,
        "numa_balancing_scan_period_max_ms": 60000,
        "numa_balancing_scan_delay_ms": 1000,
    }
    subprocess.run([f'/home/sherry/projects/sk_prokect/mldpp/mldpp/memmanagement/scripts/autonuma/update.sh {sys_config["numa_balancing_scan_size_mb"]} {sys_config["numa_balancing_scan_period_min_ms"]} {sys_config["numa_balancing_scan_period_max_ms"]} {sys_config["numa_balancing_scan_delay_ms"]}'], shell=True, text=True, check=True)
    return sys_config

def reset_random(bench_pid):
    numa_balancing_scan_size_mb = random.choice([256, 512, 1024, 2048, 4096])
    numa_balancing_scan_period_min_ms = 1000
    numa_balancing_scan_period_max_ms = 60000
    numa_balancing_scan_delay_ms = 1000

    sys_config = {
        "numa_balancing_scan_size_mb": numa_balancing_scan_size_mb,
        "numa_balancing_scan_period_min_ms": numa_balancing_scan_period_min_ms,
        "numa_balancing_scan_period_max_ms": numa_balancing_scan_period_max_ms,
        "numa_balancing_scan_delay_ms": numa_balancing_scan_delay_ms,
    }
    subprocess.run([f'/home/sherry/projects/sk_prokect/mldpp/mldpp/memmanagement/scripts/autonuma/update.sh {sys_config["numa_balancing_scan_size_mb"]} {sys_config["numa_balancing_scan_period_min_ms"]} {sys_config["numa_balancing_scan_period_max_ms"]} {sys_config["numa_balancing_scan_delay_ms"]}'], shell=True, text=True, check=True)
    return sys_config

def update_random(bench_pid):
    numa_balancing_scan_size_mb = random.choice([256, 512, 1024, 2048, 4096])
    numa_balancing_scan_period_min_ms = 1000
    numa_balancing_scan_period_max_ms = 60000
    numa_balancing_scan_delay_ms = 1000

    sys_config = {
        "numa_balancing_scan_size_mb": numa_balancing_scan_size_mb,
        "numa_balancing_scan_period_min_ms": numa_balancing_scan_period_min_ms,
        "numa_balancing_scan_period_max_ms": numa_balancing_scan_period_max_ms,
        "numa_balancing_scan_delay_ms": numa_balancing_scan_delay_ms,
    }
    subprocess.run([f'/home/sherry/projects/sk_prokect/mldpp/mldpp/memmanagement/scripts/autonuma/update.sh {sys_config["numa_balancing_scan_size_mb"]} {sys_config["numa_balancing_scan_period_min_ms"]} {sys_config["numa_balancing_scan_period_max_ms"]} {sys_config["numa_balancing_scan_delay_ms"]}'], shell=True, text=True, check=True)
    return sys_config

def update_default(bench_pid):
    sys_config = {
        "numa_balancing_scan_size_mb": 256,
        "numa_balancing_scan_period_min_ms": 1000,
        "numa_balancing_scan_period_max_ms": 60000,
        "numa_balancing_scan_delay_ms": 1000,
    }
    subprocess.run([f'/home/sherry/projects/sk_prokect/mldpp/mldpp/memmanagement/scripts/autonuma/update.sh {sys_config["numa_balancing_scan_size_mb"]} {sys_config["numa_balancing_scan_period_min_ms"]} {sys_config["numa_balancing_scan_period_max_ms"]} {sys_config["numa_balancing_scan_delay_ms"]}'], shell=True, text=True, check=True)
    return sys_config

def update_default_with_ml(predictor, bench_pid, model_name, new_datapoint, target = 'latency'):
    min_latency_neighbor ,info = predictor.find_optimal_config(new_datapoint, target)

    numa_balancing_scan_size_mb = min_latency_neighbor['numa_balancing_scan_size_mb']

    sys_config = {
        "numa_balancing_scan_size_mb": 256,
        "numa_balancing_scan_period_min_ms": 1000,
        "numa_balancing_scan_period_max_ms": 60000,
        "numa_balancing_scan_delay_ms": 1000,
    }
    subprocess.run([f'/home/sherry/projects/sk_prokect/mldpp/mldpp/memmanagement/scripts/autonuma/update.sh {sys_config["numa_balancing_scan_size_mb"]} {sys_config["numa_balancing_scan_period_min_ms"]} {sys_config["numa_balancing_scan_period_max_ms"]} {sys_config["numa_balancing_scan_delay_ms"]}'], shell=True, text=True, check=True)
    return sys_config
    
def update_ml(predictor, bench_pid, model_name, new_datapoint, target = 'latency'):
    min_latency_neighbor, info = predictor.find_optimal_config(new_datapoint, target)

    numa_balancing_scan_size_mb = int(min_latency_neighbor['numa_balancing_scan_size_mb'])
    numa_balancing_scan_period_min_ms = 1000
    numa_balancing_scan_period_max_ms = 60000
    numa_balancing_scan_delay_ms = 1000

    sys_config = {
        "numa_balancing_scan_size_mb": numa_balancing_scan_size_mb,
        "numa_balancing_scan_period_min_ms": numa_balancing_scan_period_min_ms,
        "numa_balancing_scan_period_max_ms": numa_balancing_scan_period_max_ms,
        "numa_balancing_scan_delay_ms": numa_balancing_scan_delay_ms,
    }
    subprocess.run([f'/home/sherry/projects/sk_prokect/mldpp/mldpp/memmanagement/scripts/autonuma/update.sh {sys_config["numa_balancing_scan_size_mb"]} {sys_config["numa_balancing_scan_period_min_ms"]} {sys_config["numa_balancing_scan_period_max_ms"]} {sys_config["numa_balancing_scan_delay_ms"]}'], shell=True, text=True, check=True)
    return sys_config, info

def csv_headers():
    return [
        "ldram_size(MB)",
        "numa_balancing_scan_size_mb",
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
