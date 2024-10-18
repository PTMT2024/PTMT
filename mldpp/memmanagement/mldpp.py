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
# from predictor import *

def reset(bench_pid):
    sys_config = {
        "read_sample_period": 100,
        "hotpage_threshold": 2,
        # "hotpage_threshold": 1,
        "page_migration_interval": 1,
    }
    subprocess.run([f"/home/sherry/projects/sk_prokect/mldpp/page_placement_tools/user_space_page_migration/tcp_client/client enable -p {bench_pid} -h {sys_config['hotpage_threshold']} -m {sys_config['page_migration_interval']} -d {sys_config['read_sample_period']}"], shell=True, text=True, check=True)
    return sys_config

def reset_random(bench_pid):
    read_sample_period = 100
    # read_sample_period = random.randint(1, 5) * 100
    # sample_period_mul = random.randint(1, 10) * 500
    sample_period_mul = 500
    store_sampling_period = read_sample_period * sample_period_mul
    # profiling_interval = random.randint(1, 10)
    profiling_interval = 1
    # proc_scan_interval = random.randint(1, 6) * 10
    proc_scan_interval = 0
    # page_fetch_interval = random.randint(1, 10)
    page_fetch_interval = 1
    # hotpage_threshold = random.choice([2,3,4,5,6])
    hotpage_threshold = os.environ['hotpage_threshold']
    # page_migration_interval = random.choice([1, 2, 3])
    page_migration_interval = 1

    sys_config = {
        "read_sample_period": read_sample_period,
        "sample_period_mul": sample_period_mul,
        "store_sampling_period": store_sampling_period,
        "profiling_interval": profiling_interval,
        "proc_scan_interval": proc_scan_interval,
        "page_fetch_interval": page_fetch_interval,
        "hotpage_threshold": hotpage_threshold,
        "page_migration_interval": page_migration_interval,
    }
    subprocess.run([f"/home/sherry/projects/sk_prokect/mldpp/page_placement_tools/user_space_page_migration/tcp_client/client enable -p {bench_pid} -h {sys_config['hotpage_threshold']} -m {sys_config['page_migration_interval']} -d {sys_config['read_sample_period']}"], shell=True, text=True, check=True)
    return sys_config

def update_random(bench_pid):
    read_sample_period = 100
    # read_sample_period = random.randint(1, 5) * 100
    # sample_period_mul = random.randint(1, 10) * 500
    sample_period_mul = 500
    store_sampling_period = read_sample_period * sample_period_mul
    # profiling_interval = random.randint(1, 10)
    profiling_interval = 1
    # proc_scan_interval = random.randint(1, 6) * 10
    proc_scan_interval = 0
    # page_fetch_interval = random.randint(1, 10)
    page_fetch_interval = 1
    hotpage_threshold = random.randint(2, 6)
    page_migration_interval = random.choice([1, 2, 3])
    # page_migration_interval = 1

    sys_config = {
        "read_sample_period": read_sample_period,
        "sample_period_mul": sample_period_mul,
        "store_sampling_period": store_sampling_period,
        "profiling_interval": profiling_interval,
        "proc_scan_interval": proc_scan_interval,
        "page_fetch_interval": page_fetch_interval,
        "hotpage_threshold": hotpage_threshold,
        "page_migration_interval": page_migration_interval,
    }
    subprocess.run([f"/home/sherry/projects/sk_prokect/mldpp/page_placement_tools/user_space_page_migration/tcp_client/client update -h {sys_config['hotpage_threshold']} -m {sys_config['page_migration_interval']} -d {sys_config['read_sample_period']}"], shell=True, text=True, check=True) 
    return sys_config

def update_default(bench_pid):
    sys_config = {
        "read_sample_period": 100,
        "hotpage_threshold": 2,
        "page_migration_interval": 1,
    }
    subprocess.run([f"/home/sherry/projects/sk_prokect/mldpp/page_placement_tools/user_space_page_migration/tcp_client/client update -h {sys_config['hotpage_threshold']} -m {sys_config['page_migration_interval']} -d {sys_config['read_sample_period']}"], shell=True, text=True, check=True) 
    return sys_config

def update_default_with_ml(predictor, bench_pid, model_name, new_datapoint, target = 'latency'):
    min_latency_neighbor ,info = predictor.find_optimal_config(new_datapoint, target)
    mem_quota = 0
    sample_freq = 0
    read_sample_period = 100
    # read_sample_period = random.randint(1, 5) * 100
    # sample_period_mul = random.randint(1, 10) * 500
    sample_period_mul = 500
    store_sampling_period = read_sample_period * sample_period_mul
    # profiling_interval = random.randint(1, 10)
    profiling_interval = 1
    # proc_scan_interval = random.randint(1, 6) * 10
    proc_scan_interval = 0
    # page_fetch_interval = random.randint(1, 10)
    page_fetch_interval = 1
    hotpage_threshold = min_latency_neighbor['hotpage_threshold']
    page_migration_interval = min_latency_neighbor['page_migration_interval(s)']

    sys_config = {
        "read_sample_period": 100,
        "hotpage_threshold": 2,
        "page_migration_interval": 1,
    }
    subprocess.run([f"/home/sherry/projects/sk_prokect/mldpp/page_placement_tools/user_space_page_migration/tcp_client/client update -h {sys_config['hotpage_threshold']} -m {sys_config['page_migration_interval']} -d {sys_config['read_sample_period']}"], shell=True, text=True, check=True) 
    return sys_config

def update_ml(predictor, bench_pid, model_name, new_datapoint, target = 'latency'):
    min_latency_neighbor, info = predictor.find_optimal_config(new_datapoint, target)
    mem_quota = 0
    sample_freq = 0
    read_sample_period = 100
    # read_sample_period = random.randint(1, 5) * 100
    # sample_period_mul = random.randint(1, 10) * 500
    sample_period_mul = 500
    store_sampling_period = read_sample_period * sample_period_mul
    # profiling_interval = random.randint(1, 10)
    profiling_interval = 1
    # proc_scan_interval = random.randint(1, 6) * 10
    proc_scan_interval = 0
    # page_fetch_interval = random.randint(1, 10)
    page_fetch_interval = 1
    hotpage_threshold = int(min_latency_neighbor['hotpage_threshold'])
    page_migration_interval = int(min_latency_neighbor['page_migration_interval(s)'])

    sys_config = {
        "read_sample_period": read_sample_period,
        "hotpage_threshold": hotpage_threshold,
        "page_migration_interval": page_migration_interval,
    }
    subprocess.run([f"/home/sherry/projects/sk_prokect/mldpp/page_placement_tools/user_space_page_migration/tcp_client/client update -h {sys_config['hotpage_threshold']} -m {sys_config['page_migration_interval']} -d {sys_config['read_sample_period']}"], shell=True, text=True, check=True) 
    return sys_config, info

def update_rl(predicted_combination):
    hotpage_threshold =  int(predicted_combination['hotpage_threshold'])
    page_migration_interval = int(predicted_combination['page_migration_interval(s)'])
    read_sample_period = 100

    sys_config = {
        "read_sample_period": read_sample_period,
        "hotpage_threshold": hotpage_threshold,
        "page_migration_interval": page_migration_interval,
    }
    subprocess.run([f"/home/sherry/projects/sk_prokect/mldpp/page_placement_tools/user_space_page_migration/tcp_client/client update -h {sys_config['hotpage_threshold']} -m {sys_config['page_migration_interval']} -d {sys_config['read_sample_period']}"], shell=True, text=True, check=True) 
    return sys_config

def csv_headers():
    return [
        "ldram_size(MB)",
        "hotpage_threshold",
        "page_migration_interval(s)",
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
        sys_config["hotpage_threshold"],
        sys_config["page_migration_interval"],
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
