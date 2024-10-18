
import importlib
import itertools
import random

ClassCombination = {
            "tiering08":  [
                {"numa_balancing_scan_size_mb": [256, 1024, 4096, 8192]},
                {"numa_balancing_promote_watermark_mb": [10, 64, 128 ,256, 512]}
            ],
            "autonuma": [
                {"numa_scan_size_mb": [256, 1024, 4096, 8192]},
            ],
            "mldpp": [
                {"hotpage_threshold": [2,3,4,5,6]},
                {"page_migration_interval(s)": [1, 2, 3]}
            ],
            "tpp": [
                {"demote_scale_factor": [200, 100, 400, 800]}
            ]
        }

class ActionEncoding:
    def __init__(self, memmanagement, bench_pid):
        self.memmanagement = memmanagement
        self.bench_pid = bench_pid
        self.__generate_workload_param()
        self.__generate_one_hot_encodings()
        self.memmanagement_module = importlib.import_module(f"memmanagement.{memmanagement}")

    def __generate_workload_param(self):
        self.workload_param = ClassCombination[self.memmanagement]
        self.param_names = [list(item.keys())[0] for item in self.workload_param]
        self.param_values = [list(item.values())[0] for item in self.workload_param]
        self.param_combinations = list(itertools.product(*self.param_values))

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
        print("one_hot_encodings: ", self.one_hot_encodings)
        print("one_hot_decodings: ", self.one_hot_decodings)
        print("one_hot_configs: ", self.one_hot_configs)
    
    def convert_action_to_config(self, action_index):
        params_combination  = self.one_hot_configs[action_index]
        return params_combination
    
    def random_action(self):
        return random.randint(0, len(self.one_hot_configs) - 1)
    
    def apply_action(self, action_index):
        params_combination  = self.one_hot_configs[action_index]
        return self.memmanagement_module.update_rl(params_combination)
    
    def apply_default(self):
        return self.memmanagement_module.reset(self.bench_pid)