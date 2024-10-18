import numpy as np
from dataclasses import dataclass
from sklearn.decomposition import PCA

from idt.idt_config import *
from idt.idt_action import *
from utils import *
import datetime
import pandas as pd
import importlib
import csv

class IDTState:
    def __init__ (self, logdir, ldram_size, memmanagement):
        self.logdir = logdir
        self.ldram_size = ldram_size
        self.next_state = None
        self.memmanagement_module = importlib.import_module(f"memmanagement.{memmanagement}")

    def get_state (self, current_step, sysconfig):
        logging.info(f"get_state {current_step} at {datetime.datetime.now()}") 
        self.next_state, metrics_result = self.__collect_observation(current_step)
        info = {"metrics_result": metrics_result, "config": sysconfig}
        self.__save_existing_result(info["config"], self.ldram_size, info["metrics_result"])
        return self.next_state, info

    def __collect_observation(self, curr_step):
        metrics_result = self.__parse_metrics_result(curr_step)
        previous_status =  {
            "ipc": float(metrics_result["IPC"]),
            "l3cache_misses(/us)": float(metrics_result["L3CacheMisses"]),
            "l2cache_misses(/us)": float(metrics_result["L2CacheMisses"]),
            "l3cache_hit_ratio": float(metrics_result["L3CacheHitRatio"]),
            "l2cache_hit_ratio": float(metrics_result["L2CacheHitRatio"]),
            "written_to_pmm(MB/s)":  float(metrics_result["WrittenToPMM"]),
            "written_to_dram(MB/s)":  float(metrics_result["WrittenToDRAM"]),
            "read_from_pmm(MB/s)":  float(metrics_result["ReadFromPMM"]),
            "read_from_dram(MB/s)": float(metrics_result["ReadFromDRAM"]),
            "llc_read_miss_latency(ns)": float(metrics_result["LLCReadMissLatency"]),
        }
        return self.__convert_metrics_to_obs(previous_status), metrics_result

    def __convert_metrics_to_obs(self, new_point):
        data = pd.DataFrame(new_point, index=[0])
        data['ipc'] = data['ipc'].fillna(0)

        data["pmm_ratio_of_write"] = data["written_to_pmm(MB/s)"] / (
            data["written_to_pmm(MB/s)"] + data["written_to_dram(MB/s)"]
        )
        data["pmm_ratio_of_read"] = data["read_from_pmm(MB/s)"] / (
            data["read_from_pmm(MB/s)"] + data["read_from_dram(MB/s)"]
        )
        data["total_write_traffic"] = (
            data["written_to_pmm(MB/s)"] + data["written_to_dram(MB/s)"]
        )
        data["total_read_traffic"] = (
            data["read_from_pmm(MB/s)"] + data["read_from_dram(MB/s)"]
        )
        data["total_traffic"] = data["total_write_traffic"] + data["total_read_traffic"]
        data["write_traffic_ratio"] = (
            data["total_write_traffic"] / data["total_traffic"]
        )
        data["read_traffic_ratio"] = data["total_read_traffic"] / data["total_traffic"]
        data["total_pmm_traffic"] = data["written_to_pmm(MB/s)"] + data["read_from_pmm(MB/s)"]
        data["total_dram_traffic"] = data["written_to_dram(MB/s)"] + data["read_from_dram(MB/s)"]   
        data["total_pmm_trafic_norm"] = data["total_pmm_traffic"] / (2666 * 8)
        data["total_dram_trafic_norm"] = data["total_dram_traffic"] / (2933 * 8)

        for column in data.columns:
            data[f'prev_{column}'] = data[column]
        
        obs =  data[self.prev_state_columns()].iloc[0].to_numpy()
        return obs


    def prev_state_columns(self):
        lst = [
            "pmm_ratio_of_write",
            "pmm_ratio_of_read",
            # "total_pmm_trafic_norm",
            # "total_dram_trafic_norm",
            "read_traffic_ratio",
            "l3cache_hit_ratio",
            "l2cache_hit_ratio",
        ]
        new_lst = [f'prev_{elem}' for elem in lst]
        return new_lst

    def __metrics_log(self, count):
        return f"{self.logdir}/metrics.log.{count}"

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

    def __csv_file(self):
        return f"{self.logdir}/result.csv"

    def __csv_values(self, ldram_size, sysconfig, metrics_result, workload_result):
        return self.memmanagement_module.csv_values(ldram_size, sysconfig, metrics_result, workload_result)

    def __save_existing_result(self, sysconfig, ldram_size, metrics_result):
        workload_result = {}
        logging.info (f"__save_existing_result {self.__csv_file()}")
        logging.info(f"__save_existing_result sysconfig {sysconfig}. metrics_result {metrics_result}") 
        result_values = self.__csv_values(ldram_size, sysconfig, metrics_result, workload_result)
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
            "llc_read_miss_latency(ns)": float(metrics_result["LLCReadMissLatency"]),
        }
        with open(self.__csv_file(), mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(result_values)