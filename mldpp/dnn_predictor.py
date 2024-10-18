from var import *
from dnn_model import DNN
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import itertools

ClassCombination = {
            "tiering08":  [
                {"numa_balancing_promote_watermark_mb": [10, 64, 128, 256]},
                {"numa_balancing_hot_threshold_ms": [500, 1000, 2000]}
            ],
            "autonuma": [
                {"numa_balancing_hot_threshold_ms": [250, 500, 1000, 2000, 4000]},
                {"numa_balancing_promote_rate_limit_MBps": [65536]}
            ],
            "mldpp": [
                {"hotpage_threshold": [2,3,4,5,6]},
                {"page_migration_interval(s)": [1, 2, 3]}
            ],
            "tpp": [
                {"demote_scale_factor": [200, 100, 400, 800]}
            ]
        }

class DnnPredictor:
    def __init__(self, model_name, memmanagement):
        self.memmanagement = memmanagement
        self.model_path = f"{MLDPP_DIR}/models/{model_name}"
        self.__generate_workload_param()
        self.__prepare_model()

    def __generate_workload_param(self):
        self.workload_param = ClassCombination[self.memmanagement]
        self.param_names = [list(item.keys())[0] for item in self.workload_param]
        self.param_values = [list(item.values())[0] for item in self.workload_param]
        self.param_combinations = list(itertools.product(*self.param_values))

    def find_optimal_config(self, new_point,  target = 'latency'):
        new_datapoint = self.__process_new_point(new_point, self.top_features)
        X_test = torch.tensor(new_datapoint.values, dtype=torch.float32)
        self.model.eval()
        with torch.no_grad():
            output = self.model(X_test)
            _, predicted = torch.max(output.detach(), 1)
        return self.one_hot_configs[predicted[0].item()], {}

    def __prepare_model(self):
        self.model = DNN(len(self.param_combinations))
        self.model.load_state_dict(torch.load(self.model_path))

        self.top_features = [
            "prev_pmm_ratio_of_write",
            "prev_pmm_ratio_of_read",
            "prev_total_pmm_trafic_norm",
            "prev_total_dram_trafic_norm",
            "prev_read_traffic_ratio",
            "prev_l3cache_hit_ratio",
            "prev_l2cache_hit_ratio",
        ]
        self.__generate_one_hot_encodings()

    def __generate_one_hot_encodings(self):
        one_hot_encodings = {}
        one_hot_decodings = {}
        one_hot_configs = {}

        for class_label, param_combination in enumerate(self.param_combinations):
            one_hot_encodings[param_combination] = class_label
            one_hot_decodings[class_label] = param_combination
            one_hot_configs[class_label] = {
                key: value for key, value in zip(self.param_names, param_combination)
            }

        self.one_hot_encodings =  one_hot_encodings
        self.one_hot_decodings = one_hot_decodings
        self.one_hot_configs = one_hot_configs
        # print("one_hot_encodings: ", self.one_hot_encodings)
        # print("one_hot_decodings: ", self.one_hot_decodings)
        # print("one_hot_configs: ", self.one_hot_configs)

        
    def __process_new_point(self, new_point, top_features):
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
        
        # print(data[top_features])
        return data[top_features]