import importlib
import os
import subprocess
import datetime
import random
import csv
from utils import *
import datetime
from time import sleep

class OneDefaultTuner:
    def __init__(self, workload, memmanagement, bench, logdir, collectperiod):
        self.workload = workload
        self.memmanagement = memmanagement
        self.bench = bench
        self.logdir = logdir
        self.memmanagement_module = importlib.import_module(f"memmanagement.{memmanagement}")
        self.collect_period = int(collectperiod)
        self.start_workload_cmd = start_workload_cmd(self.memmanagement, self.bench, self.__workload_log(0), self.workload)
        self.previous_status = {}
    
    def __workload_pid_file(self):
        return f"{self.logdir}/workload.pid"

    def __csv_file(self):
        return f"{self.logdir}/result.csv"

    def __tune_log(self, count):
        return f"{self.logdir}/tune.log.{count}"

    def __workload_log(self, count):
        return f"{self.logdir}/workload.log.{count}"

    def __metrics_log(self, count):
        return f"{self.logdir}/metrics.log.{count}"

    def __csv_headers(self):
        return self.memmanagement_module.csv_headers()
    
    def __model_name(self):
        suffixes = ['_l', '_s', '_x']
        workload_name = self.workload
        for suffix in suffixes:
            if workload_name.endswith(suffix):
                workload_name = workload_name.split('_')[0]  # Keep only the part before the first '_'
                break
        return f"model.{workload_name}.{self.memmanagement}.knn_model.latency.{self.collect_period}s.pkl"
    
    def __csv_values(self, ldram_size, random_config, metrics_result, workload_result):
        return self.memmanagement_module.csv_values(ldram_size, random_config, metrics_result, workload_result)
    
    def __reset_mm_config(self, bench_pid):
        return self.memmanagement_module.reset(bench_pid)

    def __update_mm_config_random(self, bench_pid):
        return self.memmanagement_module.update_random(bench_pid)
    
    def __update_mm_config_ml(self, bench_pid, model_name, new_datapoint):
        return self.memmanagement_module.update_ml(bench_pid, model_name, new_datapoint)
    
    def __update_mm_config_default(self, bench_pid):
        return self.memmanagement_module.update_default(bench_pid)

    def __save_result(self, count, random_config, ldram_size):
        metrics_result = self.__parse_metrics_result(count)
        # workload_result = self.__parse_workload_result(count)
        workload_result = {}

        result_values = self.__csv_values(ldram_size, random_config, metrics_result, workload_result)
        self.previous_status =  {
            "ipc": float(metrics_result["IPC"]),
            "l3cache_misses(/us)": float(metrics_result["L3CacheMisses"]),
            "l2cache_misses(/us)": float(metrics_result["L2CacheMisses"]),
            "l3cache_hit_ratio": float(metrics_result["L3CacheHitRatio"]),
            "l2cache_hit_ratio": float(metrics_result["L2CacheHitRatio"]),
            "written_to_pmm(MB/s)":  float(metrics_result["WrittenToPMM"]),
            "written_to_dram(MB/s)":  float(metrics_result["WrittenToDRAM"]),
            "read_from_pmm(MB/s)":  float(metrics_result["ReadFromPMM"]),
            "read_from_dram(MB/s)": float(metrics_result["ReadFromDRAM"]),
        }
        with open(self.__csv_file(), mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(result_values)

    def __parse_workload_result(self, count):
        output = subprocess.check_output(
            f"cat {self.__workload_log(count)}", shell=True, text=True
        )
        workload_result = {}
        for line in output.splitlines():
            if "Time in seconds =" in line:
                workload_result["ExecutionTime"] = line.split(" ")[-1]
        return workload_result

    def __parse_metrics_result(self, count):
        print(f"cat {self.__metrics_log(count)} at {datetime.datetime.now()}")
        output = reliable_cat(self.__metrics_log(count))
        metrics_result = {}
        for line in output.splitlines():
            if "ExecutionTime" in line:
                metrics_result["ExecutionTime"] = line.split(" ")[1]
            elif "IPC" in line:
                metrics_result["IPC"] = line.split(" ")[1]
            elif "IPUS" in line:
                metrics_result["IPUS"] = line.split(" ")[1]
            elif "Instructions" in line:
                metrics_result["Instructions"] = line.split(" ")[1]
            elif "Cycles" in line:
                metrics_result["Cycles"] = line.split(" ")[1]
            elif "WrittenToPMM" in line:
                metrics_result["WrittenToPMM"] = line.split(" ")[1]
            elif "ReadFromPMM" in line:
                metrics_result["ReadFromPMM"] = line.split(" ")[1]
            elif "WrittenToDRAM" in line:
                metrics_result["WrittenToDRAM"] = line.split(" ")[1]
            elif "ReadFromDRAM" in line:
                metrics_result["ReadFromDRAM"] = line.split(" ")[1]
            elif "L2CacheMisses" in line:
                metrics_result["L2CacheMisses"] = line.split(" ")[1]
            elif "L3CacheMisses" in line:
                metrics_result["L3CacheMisses"] = line.split(" ")[1]
            elif "L2CacheHitRatio" in line:
                metrics_result["L2CacheHitRatio"] = line.split(" ")[1]
            elif "L3CacheHitRatio" in line:
                metrics_result["L3CacheHitRatio"] = line.split(" ")[1]
            elif "LLCReadMissLatency" in line:
                metrics_result["LLCReadMissLatency"] = line.split(" ")[1]
        return metrics_result

    def __run_and_collect(self, count, bench_pid, ldram_size):
        random_config = {}
        if count == 1:
            random_config = self.__reset_mm_config(bench_pid) 
        else:
            random_config = self.__update_mm_config_default(bench_pid)

        wait_workload(bench_pid, 0)
        # print('random_config:', random_config)
        self.__save_result(count, random_config, ldram_size)
        print(f"__run_and_collect {count} times")

    def __create_result_csv(self):
        if not os.path.exists(self.__csv_file()):
            with open(self.__csv_file(), mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.__csv_headers())

    def __read_workload_pid(self):
        try:
            with open(self.__workload_pid_file(), 'r') as f:
                workload_pid = int(f.read().strip())
            return workload_pid
        except FileNotFoundError:
            print("Failed to find workload PID file")
            exit(1)

    def __prepare(self):
        
        self.__create_result_csv()
        os.environ['OMP_NUM_THREADS'] = '24'
        os.environ['LOG_DIR'] = self.logdir
        # if self.memmanagement == "mldpp":
        #     with open(self.__tune_log(0), 'w') as f:
        #         user_space_page_migration = subprocess.Popen(["/home/sherry/projects/sk_prokect/mldpp/page_placement_tools/user_space_page_migration/user_space_page_migration", "-w", "0", "-q", "0"], stdout=f, stderr=subprocess.STDOUT)
        #         # print("PID of user_space_page_migration: ", user_space_page_migration.pid)

    def do(self):
        self.__prepare()
        ldram_size = get_numa_free_memory()[0]
        bench_process = subprocess.Popen(self.start_workload_cmd, shell=True)
        # with open(self.__workload_log(0), 'w') as f:
        #     bench_process = subprocess.Popen(self.bench, stdout=f, stderr=subprocess.STDOUT)        
        sleep(2)
        bench_pid = self.__read_workload_pid()
        print("PID of workload: ", bench_pid)
        if self.workload == "Silo":
            pebs_target_pid = -1
        else:
            pebs_target_pid = bench_pid
        collect_metrics_cmd = f"/home/sherry/projects/sk_prokect/mldpp/collector/mldpp_metrics_collector 0 {bench_pid} 0 {pebs_target_pid} {self.logdir}"
        metrics_collector_proc = subprocess.Popen(collect_metrics_cmd, shell=True)
        print("collect_metrics_cmd: ", collect_metrics_cmd)
        sleep(4)

        count = 1
        self.__run_and_collect(count, bench_pid, ldram_size)

        # if self.memmanagement == "mldpp":
        #     user_space_page_migration.wait()
        bench_process.wait()
        sleep(10)
        print("finished")