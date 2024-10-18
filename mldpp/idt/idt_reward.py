import math
import random
import time
from dataclasses import dataclass

from idt.idt_config import *
from idt.idt_action import *
from idt.idt_state import *
from utils import *


class Reward:
    """
    Calculate reward.

    Action should be applied before invoking `get_reward`.
    Reward is calculated after waiting for collect_period to 'fully' apply action.
    """

    min_ipc = 0.02
    max_ipc = 2

            
    @staticmethod
    def wait_for_reward (collect_period):
        wait_workload(0, collect_period)



    @staticmethod
    def get_reward (metrics_result):
        """
        Get reward when action is applied.

        Always call wait_for_reward before invoking.

        Step 1. Wait by invoking `__wait()`.
        Step 2. Calculate reward function.

        """
        ipc = float(metrics_result["IPC"])
        reward = 2 * ((ipc - Reward.min_ipc) / (Reward.max_ipc - Reward.min_ipc)) - 1


        return reward
