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
        "demote_scale_factor": 200,
    }
    subprocess.run([f'/home/sherry/projects/sk_prokect/mldpp/mldpp/memmanagement/scripts/tpp/update.sh {sys_config["demote_scale_factor"]}'], shell=True, text=True, check=True)
    return sys_config

def reset_random(bench_pid):
    # demote_scale_factor = random.choice([200, 100, 400, 800])
    # demote_scale_factor = random.choice([800])
    demote_scale_factor = os.environ['demote_scale_factor']

    sys_config = {
        "demote_scale_factor": demote_scale_factor,
    }
    subprocess.run([f'/home/sherry/projects/sk_prokect/mldpp/mldpp/memmanagement/scripts/tpp/update.sh {sys_config["demote_scale_factor"]}'], shell=True, text=True, check=True)
    return sys_config

def update_random(bench_pid):
    demote_scale_factor = random.choice([200, 100, 400, 800])

    sys_config = {
        "demote_scale_factor": demote_scale_factor,
    }
    subprocess.run([f'/home/sherry/projects/sk_prokect/mldpp/mldpp/memmanagement/scripts/tpp/update.sh {sys_config["demote_scale_factor"]}'], shell=True, text=True, check=True)
    return sys_config

def update_default(bench_pid):
    demote_scale_factor = 200

    sys_config = {
        "demote_scale_factor": demote_scale_factor,
    }
    subprocess.run([f'/home/sherry/projects/sk_prokect/mldpp/mldpp/memmanagement/scripts/tpp/update.sh {sys_config["demote_scale_factor"]}'], shell=True, text=True, check=True)
    return sys_config

def update_default_with_ml(predictor, bench_pid, model_name, new_datapoint, target = 'latency'):
    min_latency_neighbor ,info = predictor.find_optimal_config(new_datapoint, target)

    demote_scale_factor = min_latency_neighbor['demote_scale_factor']

    sys_config = {
        "demote_scale_factor": demote_scale_factor,
    }
    subprocess.run([f'/home/sherry/projects/sk_prokect/mldpp/mldpp/memmanagement/scripts/tpp/update.sh {sys_config["demote_scale_factor"]}'], shell=True, text=True, check=True)
    return sys_config
    
def update_ml(predictor, bench_pid, model_name, new_datapoint, target = 'latency'):
    min_latency_neighbor, info = predictor.find_optimal_config(new_datapoint, target)

    demote_scale_factor = int(min_latency_neighbor['demote_scale_factor'])

    sys_config = {
        "demote_scale_factor": demote_scale_factor,
    }
    subprocess.run([f'/home/sherry/projects/sk_prokect/mldpp/mldpp/memmanagement/scripts/tpp/update.sh {sys_config["demote_scale_factor"]}'], shell=True, text=True, check=True)
    return sys_config, info

def update_rl(predicted_combination):
    demote_scale_factor =  int(predicted_combination['demote_scale_factor'])

    sys_config = {
        "demote_scale_factor": demote_scale_factor,
    }
    subprocess.run([f'/home/sherry/projects/sk_prokect/mldpp/mldpp/memmanagement/scripts/tpp/update.sh {sys_config["demote_scale_factor"]}'], shell=True, text=True, check=True)
    return sys_config

def csv_headers():
    return [
        "ldram_size(MB)",
        "demote_scale_factor",
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
        sys_config["demote_scale_factor"],
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
