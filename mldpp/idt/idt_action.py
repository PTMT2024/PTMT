import numpy as np
import random
import time

from idt.idt_config import *
from idt.idt_state import *
from utils import *
from idt.idt_action_encoding import *
from var import *


class Action:
    """
    Change paramerted by action.
    """
    idt_action = 0
    action_encodings = None

    @staticmethod
    def __init__ (memmanagement, bench_pid):
        Action.action_encodings = ActionEncoding(memmanagement, bench_pid)

    @staticmethod
    def nn_to_action (nn_out):
        """
        NN output to action.
        """

        action_idx = np.argmax(nn_out)


        return action_idx
        

    @staticmethod
    def apply_action (action_idx):
        """
        Apply action
        When using NN output, call nn_to_action before invoking.
        """
        return Action.action_encodings.apply_action(action_idx) 

    @staticmethod
    def apply_default ():
        """
        Apply default parameters
        """
        return Action.action_encodings.apply_default() 

    @staticmethod
    def random_action ():
        """
        Select random action.

        apply_action shoulb be called to actually 'apply' action.

        :return: randomly select action.
        """

        action_idx =  Action.action_encodings.random_action()

        return action_idx
    

    @staticmethod
    def print (action):
        """Print current action """

        logging.info(f"Action: {action}, {Action.action_encodings.convert_action_to_config(action)}")
