from var import *
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import itertools
import csv
import time
import gymnasium as gym
from gymnasium import spaces
# from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import A2C, PPO
from utils import *
import json
import importlib
from stable_baselines3.common.policies import obs_as_tensor
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.logger import configure
from datetime import datetime


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


class ParametersTuningEnv(gym.Env):
    def __init__(self, env_params, memmanagement, collect_period, logdir, ldram_size, bench_pid, hybrid_mode, current_step, offline=False):
        super(ParametersTuningEnv, self).__init__()
        
        self.memmanagement = memmanagement
        self.memmanagement_module = importlib.import_module(f"memmanagement.{memmanagement}")
        self.logdir = logdir
        self.offline = offline
        self.bench_pid = bench_pid
        self.ldram_size = ldram_size
        self.collect_period = collect_period
        self.hybrid_mode = hybrid_mode
        self.__generate_workload_param()
        self.__generate_one_hot_encodings()

        self.current_step = current_step
        self.action_space = spaces.Discrete(len(self.param_combinations))
        self.observation_space = spaces.Box(low=0, high=1, shape=(5,), dtype=np.float32)

        self.min_ipc = env_params["min_ipc"]
        self.max_ipc = env_params["max_ipc"]

        print(f"Min IPC: {self.min_ipc}, Max IPC: {self.max_ipc}")

    def __generate_workload_param(self):
        self.workload_param = ClassCombination[self.memmanagement]
        self.param_names = [list(item.keys())[0] for item in self.workload_param]
        self.param_values = [list(item.values())[0] for item in self.workload_param]
        self.param_combinations = list(itertools.product(*self.param_values))

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

    def reward_columns(self):
            return "ipc"

    def action_columns(self):
        return "one_hot"

    def step(self, action):
        start_time = time.time()
        print(f"Step Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
        sys_config = self.send_action(action)
        end_time = time.time()
        # Convert time to microseconds
        consuming_time_us = (end_time - start_time) * 1_000_000
        print(f"Action consuming time: {consuming_time_us:.2f} µs")
        wait_workload(0, self.collect_period)

        start_time = time.time()
        self.next_state, metrics_result = self.__collect_observation(self.current_step)
        end_time = time.time()
        # Convert time to microseconds
        consuming_time_us = (end_time - start_time) * 1_000_000
        print(f"Collect observation consuming time: {consuming_time_us:.2f} µs")
        ipc = float(metrics_result["IPC"])
        # Normalize IPC to [-1, 1]
        self.reward = 2 * ((ipc - self.min_ipc) / (self.max_ipc - self.min_ipc)) - 1
        terminated = False  # Update based on actual condition
        try:
            os.kill(self.bench_pid, 0)
        except OSError:
            print("workload finished")
            terminated = True
        truncated = False  # we do not limit the number of steps here
        info = {"metrics_result": metrics_result, "config": sys_config}

        msg = f"Step {self.current_step}: Reward: {self.reward}, Terminated: {terminated}, Truncated: {truncated}, Info: {info}"
        print(msg)
        self.__save_existing_result(info["config"], self.ldram_size, info["metrics_result"])
        return self.next_state, self.reward, terminated, truncated, info

    def send_action(self, action):
        self.current_step += 1
        action_index = action.item() 
        params_combination  = self.one_hot_configs[action_index]
        sys_config = self.memmanagement_module.update_rl(params_combination)
        print(f"Step {self.current_step}: Sending action {action_index} Config: {params_combination}")
        return sys_config
    
    def __reset_mm_config(self, bench_pid):
        return self.memmanagement_module.reset(bench_pid)

    def reset(self, seed=None, options=None):
        if not self.hybrid_mode:
            random_config = self.__reset_mm_config(self.bench_pid) 
            wait_workload(0, self.collect_period)
        self.next_state, metrics_result = self.__collect_observation(self.current_step)
        info = {"metrics_result": metrics_result, "config": random_config}
        self.__save_existing_result(info["config"], self.ldram_size, info["metrics_result"])
        return self.next_state, info

    def render(self, mode='human', close=False):
        pass
    
    def __collect_observation(self, curr_step):
        metrics_result = self.__parse_metrics_result(curr_step + 1)
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

    def __csv_file(self):
        return f"{self.logdir}/result.csv"

    def __csv_values(self, ldram_size, random_config, metrics_result, workload_result):
        return self.memmanagement_module.csv_values(ldram_size, random_config, metrics_result, workload_result)

    def __save_existing_result(self, random_config, ldram_size, metrics_result):
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
            "llc_read_miss_latency(ns)": float(metrics_result["LLCReadMissLatency"]),
        }
        with open(self.__csv_file(), mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(result_values)


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


    def __metrics_log(self, count):
        return f"{self.logdir}/metrics.log.{count}"

    def __parse_metrics_result(self, count):
        print(f"cat {self.__metrics_log(count)} at {datetime.now()}")
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

# class SaveOnBestTrainingRewardCallback(BaseCallback):
#     def __init__(self, logdir: str, verbose: int = 1):
#         super().__init__(verbose)
#         self.logdir = logdir

#     def _init_callback(self) -> None:
#         pass

#     def _on_step(self) -> bool:
#         # If your callback returns False, training is aborted early.
#         try:
#             os.kill(bench_pid, 0)
#         except OSError:
#             print("workload finished")
#             return false
        
#     def __save_existing_result(self, count, config, ldram_size, metrics_result):
#         with open(f"{self.logdir}/results.csv", "a") as file:
#             file.write(
#                 f"{count}, {ldram_size}, {config}, {metrics_result['IPC']}, {metrics_result['ExecutionTime']}\n"
#             )
#     __save_existing_result(count,  info["config"], ldram_size, info["metrics_result"])
        


class RLPredictorWOPretrain:
    def __init__(self, model_name, memmanagement, collect_period, logdir, ldram_size, bench_pid, hybrid_mode=False, current_step=0):
        self.memmanagement = memmanagement
        self.model_path = f"{MLDPP_DIR}/models/{model_name}"
        self.logdir = logdir
        self.collect_period = collect_period
        self.ldram_size = ldram_size
        self.bench_pid = bench_pid
        self.hybrid_mode = hybrid_mode
        self.__prepare_model()
        self.current_step = current_step

    def update_config(self):
        # # for debug
        # obs = obs_as_tensor(self.env.next_state, self.model.policy.device)
        # dis = self.model.policy.get_distribution(obs)
        # probs = dis.distribution.probs
        # probs_np = probs.detach().numpy()

        start_time = time.time()
        action, _state = self.model.predict(self.env.next_state, deterministic=True )
        end_time = time.time()
        # Convert time to microseconds
        consuming_time_us = (end_time - start_time) * 1_000_000
        print(f"Predict consuming time: {consuming_time_us:.2f} µs")

        obs, reward,  terminated, truncated, info = self.env.step(action)
        # print(f"Step: {self.env.current_step}, Action: {action}, Reward: {reward}, Done: {terminated}, Metrics: {info['metrics_result']}")
        return obs, reward,  terminated, truncated, info
    
    def reset(self):
        return self.env.reset()
    
    def learn(self):
        timesteps = 1e5
        self.model.learn(total_timesteps=int(timesteps))

    def __prepare_model(self):
        env_params_file_path = f"{self.model_path}.env_params.json"
        with open(env_params_file_path, 'r') as file:
            env_params = json.load(file)
        print(f"Loaded env_params: {env_params}")
        if self.hybrid_mode:
            current_step = self.current_step
        else:
            current_step = 0
        env = ParametersTuningEnv(env_params, self.memmanagement, self.collect_period, self.logdir, self.ldram_size, self.bench_pid, self.hybrid_mode, current_step, offline=False)
        self.env = env
        self.model = PPO("MlpPolicy", 
                                env=env, 
                                gamma=0.9, 
                                learning_rate=0.01,
                                n_steps=4,
                                batch_size=4,
                                verbose=1,
                                n_epochs=10,
                                )


        new_logger = configure(self.logdir, ["stdout", "csv"])
        self.model.set_logger(new_logger)

        # check PPO parameters
        print(f"Discount factor: {self.model.gamma}")
        print(f"Learning rate: {self.model.learning_rate}")
        print(f"n_steps: {self.model.n_steps}")
        print(f"batch_size: {self.model.batch_size}")
        # self.callback =  RLTrainingCallback(check_freq=1000, logdir=logdir)



