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
        f'/home/sherry/projects/sk_prokect/mldpp/mldpp/memmanagement/scripts/memtis/update.sh '
        f'{sys_config["memtis_htmm_thres_hot"]} '
        f'{sys_config["memtis_htmm_adaptation_period"]} '
        f'{sys_config["memtis_htmm_demotion_period_in_ms"]} '
        f'{sys_config["memtis_htmm_promotion_period_in_ms"]} '
        f'{sys_config["memtis_htmm_cooling_period"]} '
        f'{sys_config["memtis_htmm_gamma"]} '
        f'{sys_config["memtis_htmm_ksampled_soft_cpu_quota"]} '

    ], shell=True, text=True, check=True)

def update_config_cmd(sys_config):
    subprocess.run([
        f'/home/sherry/projects/sk_prokect/mldpp/mldpp/memmanagement/scripts/memtis/update.sh '
        f'{sys_config["memtis_htmm_thres_hot"]} '
        f'{sys_config["memtis_htmm_adaptation_period"]} '
        f'{sys_config["memtis_htmm_demotion_period_in_ms"]} '
        f'{sys_config["memtis_htmm_promotion_period_in_ms"]} '
        f'{sys_config["memtis_htmm_cooling_period"]} '
        f'{sys_config["memtis_htmm_gamma"]} '
        f'{sys_config["memtis_htmm_ksampled_soft_cpu_quota"]} '
    ], shell=True, text=True, check=True)


def reset(bench_pid):
    sys_config = {
        "memtis_htmm_thres_hot": 1,
        "memtis_htmm_adaptation_period": 100000,
        "memtis_htmm_demotion_period_in_ms": 500,
        "memtis_htmm_promotion_period_in_ms": 500,
        "memtis_htmm_cooling_period": 2000000,
        "memtis_htmm_gamma": 4,
        "memtis_htmm_ksampled_soft_cpu_quota": 30,
    }
    reset_config_cmd(sys_config)
    return sys_config

def reset_random(bench_pid):
    sys_config = {
        "memtis_htmm_thres_hot": 1,
        "memtis_htmm_adaptation_period": 100000,
        # "memtis_htmm_adaptation_period": random.choice([1000, 100000, 500000, 1000000]),
        # "memtis_htmm_promotion_period_in_ms": 500,
        "memtis_htmm_promotion_period_in_ms": random.choice([250]),        "memtis_htmm_demotion_period_in_ms": 500,
        # "memtis_htmm_demotion_period_in_ms": random.choice([250, 500, 1000, 10000]),
        # "memtis_htmm_cooling_period": random.choice([2000, 2000000, 4000000]),
        "memtis_htmm_cooling_period": 2000000,
        "memtis_htmm_gamma": 4,
        "memtis_htmm_ksampled_soft_cpu_quota": 30,
        # "memtis_htmm_ksampled_soft_cpu_quota": random.choice([10, 30, 90]),
    }
    reset_config_cmd(sys_config)
    return sys_config

def update_random(bench_pid):
    sys_config = {
        "memtis_htmm_thres_hot": 1,
        "memtis_htmm_adaptation_period": 100000,
        "memtis_htmm_demotion_period_in_ms": random.choice([250, 500, 1000, 2000, 4000]),
        "memtis_htmm_promotion_period_in_ms": random.choice([250, 500, 1000, 2000, 4000]),
        "memtis_htmm_cooling_period": 2000000,
        "memtis_htmm_gamma": 4,
        "memtis_htmm_ksampled_soft_cpu_quota": 30,
    }
    update_config_cmd(sys_config)
    return sys_config

def update_default(bench_pid):
    sys_config = {
        "memtis_htmm_thres_hot": 1,
        "memtis_htmm_adaptation_period": 100000,
        "memtis_htmm_demotion_period_in_ms": 500,
        "memtis_htmm_promotion_period_in_ms": 500,
        "memtis_htmm_cooling_period": 2000000,
        "memtis_htmm_gamma": 4,
        "memtis_htmm_ksampled_soft_cpu_quota": 30,
    }
    update_config_cmd(sys_config)
    return sys_config

def update_default_with_ml(predictor, bench_pid, model_name, new_datapoint, target = 'latency'):
    min_latency_neighbor ,info = predictor.find_optimal_config(new_datapoint, target)
    memtis_htmm_demotion_period_in_ms = int(min_latency_neighbor['memtis_htmm_demotion_period_in_ms'])
    memtis_htmm_promotion_period_in_ms = int(min_latency_neighbor['memtis_htmm_promotion_period_in_ms'])

    sys_config = {
        "memtis_htmm_thres_hot": 1,
        "memtis_htmm_adaptation_period": 100000,
        "memtis_htmm_demotion_period_in_ms": 500,
        "memtis_htmm_promotion_period_in_ms": 500,
        "memtis_htmm_cooling_period": 2000000,
        "memtis_htmm_gamma": 4,
        "memtis_htmm_ksampled_soft_cpu_quota": 30,
    }
    update_config_cmd(sys_config)
    return sys_config
    
def update_ml(predictor, bench_pid, model_name, new_datapoint, target = 'latency'):
    min_latency_neighbor, info = predictor.find_optimal_config(new_datapoint, target)
    memtis_htmm_demotion_period_in_ms = int(min_latency_neighbor['memtis_htmm_demotion_period_in_ms'])
    memtis_htmm_promotion_period_in_ms = int(min_latency_neighbor['memtis_htmm_promotion_period_in_ms'])

    sys_config = {
        "memtis_htmm_thres_hot": 1,
        "memtis_htmm_adaptation_period": 100000,
        "memtis_htmm_demotion_period_in_ms": memtis_htmm_demotion_period_in_ms,
        "memtis_htmm_promotion_period_in_ms": memtis_htmm_promotion_period_in_ms,
        "memtis_htmm_cooling_period": 2000000,
        "memtis_htmm_gamma": 4,
        "memtis_htmm_ksampled_soft_cpu_quota": 30,
    }
    update_config_cmd(sys_config)
    return sys_config, info

def csv_headers():
    return [
        "ldram_size(MB)",
        "memtis_htmm_thres_hot",
        "memtis_htmm_adaptation_period",
        "memtis_htmm_demotion_period_in_ms",
        "memtis_htmm_promotion_period_in_ms",
        "memtis_htmm_cooling_period",
        "memtis_htmm_gamma",
        "memtis_htmm_ksampled_soft_cpu_quota",
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
        sys_config["memtis_htmm_thres_hot"],
        sys_config["memtis_htmm_adaptation_period"],
        sys_config["memtis_htmm_demotion_period_in_ms"],
        sys_config["memtis_htmm_promotion_period_in_ms"],
        sys_config["memtis_htmm_cooling_period"],
        sys_config["memtis_htmm_gamma"],
        sys_config["memtis_htmm_ksampled_soft_cpu_quota"],
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
