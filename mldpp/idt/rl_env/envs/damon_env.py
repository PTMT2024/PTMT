import gym
import numpy as np
import random

from idt.idt_action import *
from idt.idt_state import *
from idt.idt_reward import *
from idt.experience import *

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

class DAMON_v0 (gym.Env):
    """Environment for RL training. Set 'select_env=damon-v0' to use.

    DAMON_v0 gets state, reward, and action from the experience buffer.
    The values are calculated when storing in the experience buffer.
    """

    metadata = { "render.modes": ["human"] }

    def __init__(self,memmanagement, collect_period, logdir, ldram_size, bench_pid):
        self.memmanagement = memmanagement
        self.memmanagement_module = importlib.import_module(f"memmanagement.{memmanagement}")
        self.logdir = logdir
        self.bench_pid = bench_pid
        self.ldram_size = ldram_size
        self.collect_period = collect_period
        self.__generate_workload_param()

        self.current_step = 0
        self.action_space = gym.spaces.Discrete(len(self.param_combinations))
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(5,), dtype=np.float32)

        self.reset()


    def __generate_workload_param(self):
        self.workload_param = ClassCombination[self.memmanagement]
        self.param_names = [list(item.keys())[0] for item in self.workload_param]
        self.param_values = [list(item.values())[0] for item in self.workload_param]
        self.param_combinations = list(itertools.product(*self.param_values))


    def __get_state (self, experience):
        return Experience.get_state(experience)


    def __get_reward (self, experience):
        return Experience.get_reward(experience)


    def reset (self):
        """Reset environment.
        Configured as OpenAI Gym doc.

        :return: state
        """

        # Reset env state & reward
        self.state = np.array([0.0] * 5, dtype=np.float32)
        self.reward = 0
        self.done = False
        self.info = {}

        self.experience_buf = Experience.read() 

        return self.state

    def step (self, action):
        """Step action.
        Configured as OpenAI Gym doc.

        Step 1. Read random entry from experience_buf
        Step 2. Obtain state, reward from the entry
        Step 3. Delete read entry

        :return: [state, reward, done, info]
        """

        if self.experience_buf:
            key, experience = random.choice(list(self.experience_buf.items()))
            self.state = self.__get_state(experience)
            self.reward = self.__get_reward(experience)
        else:
            self.state = np.array([0.0] * 5, dtype=np.float32)
            self.reward = 0

        return [self.state, self.reward, self.done, self.info]


    def close (self):
        pass
