import random

from idt.idt_config import *
from idt.rl_config import *
from idt.idt_state import *
from idt.idt_action import *
from idt.idt_reward import *
from utils import *
from idt.experience import *
from idt.train import *


class Infer:
    """
    Infer using trained RL model.
    
    Infer by the trained RL model. Infer module collects the state and applies action online. (Recall that training utilizes experience buffer data) 
    Step 1. Collect current state.
    Step 2. Use trained model to determine action for current state.
    Step 3. Apply action.
    Step 4. Wait for Action.action_apply_wait seconds. This is to wait for action to be 'fully' applied.
    Step 5. Calculate reward.
    Step 6. Save to state, action, reward to the experience buffer.
    Step 7. Later, train module trains from the experience buffer.
    """

    # probability of choosing random action instead of using trained model
    rand_p = 0.05
    # train
    # rand_p = 0.95

    def __init__ (self, need_restore, memmanagement, bench_pid, collect_period, logdir, ldram_size, idt_state, chkpt_file, select_env="damon-v0"):
        logging.info("Infer initializing.")

        rl_config = RL_Config(memmanagement, collect_period, logdir, ldram_size, bench_pid)
        rl_config.rllib_init(select_env)
        self.collect_period = collect_period
        self.memmanagement = memmanagement
        self.bench_pid = bench_pid
        self.idt_state = idt_state
        self.agent = rl_config.rllib_agent_config(1, select_env)
        logging.info("agent =======")
        logging.info(self.agent.get_policy().model)
        self.need_restore = need_restore

        if self.need_restore:
            try:
                self.agent.restore(chkpt_file)
            except Exception as e:
                # Log the error or handle it as needed
                print(f"Skipping due to error: {e}")

        # Print iteration and epoch counts
        # self.print_training_info()

        self.policy = self.agent.get_policy()
        self.model = self.policy.model
        self.current_step = 0

        Action.__init__(self.memmanagement, self.bench_pid)
        logging.info("Infer initialize complete.")
        # raise


    def __infer (self):
        """
        Infer by using trained model or randomly selecting action.
        
        Step 1. Get state.
        Step 2. For p < rand_p, choose random action and get reward by Reward.get_reward.
        Step 3. Apply action by RL model.
        Step 4. Get reward by actually write action to proc/idt_action and calculate reward function by Reward.get_reward.
        Step 5. Save to the expereince buffer.

        """
        
        timer = Timer()
        timer.start()

        if random.random() >= Infer.rand_p:
            # nn_out = self.agent.compute_single_action(self.state)
            # logging.info(f"NN out: {nn_out}")
            # action = Action.nn_to_action(nn_out)
            action = self.agent.compute_single_action(self.state)
            logging.info(f"Action {action} selected.")
            sysconfig = Action.apply_action(action)
        else:
            action = Action.random_action()
            logging.info(f"Random action {action} selected.")
            sysconfig = Action.apply_action(action)
        
        Action.print(action)

        timer.end()
        timer.print()

        return (self.state, action, sysconfig)

    
    def infer (self):
        terminated = False 
        try:
            os.kill(self.bench_pid, 0)
        except OSError:
            logging.info("workload finished")
            terminated = True
            return terminated
        logging.info("Infer start\n")
        old_state, action, sysconfig = self.__infer()
        self.current_step += 1
        Reward.wait_for_reward(self.collect_period)
        state, info = self.idt_state.get_state(self.current_step + 1, sysconfig)
        reward = Reward.get_reward(info["metrics_result"])
        Experience.save(old_state, reward, action)
        self.state = state
        logging.info("Infer finish\n\n")
        return terminated


    def print_training_info(self):
        trainer_state = self.agent.__getstate__()
        print(f"Training info: {trainer_state}")

        # Extract and print iterations count
        iterations_count = trainer_state.get("num_iters", "N/A")
        print(f"Number of iterations: {iterations_count}")

        # Extract and print epochs count
        # Note: RLlib does not typically use "epochs" terminology, but you might refer to the number of SGD iterations per training iteration
        config = self.agent.config
        epochs_per_iteration = config.get("num_sgd_iter", "N/A")
        print(f"Number of epochs per iteration: {epochs_per_iteration}")

    def reset (self):
        sysconfig = Action.apply_default() 
        Reward.wait_for_reward(self.collect_period)
        state, info = self.idt_state.get_state(self.current_step + 1, sysconfig)
        self.state = state

        return self.state, info
    

    def load_mdl_and_reset_experience(self, chkpt_file):
        """
        Reset by loading the newly trained model and reset the experience buffer.

        :param chkpt_file: model to be restored
        """     
        if self.need_restore:
            try:
                self.agent.restore(chkpt_file)
            except Exception as e:
                # Log the error or handle it as needed
                print(f"Skipping due to error: {e}")
            logging.info(f"Model restored from {chkpt_file}.")
        Experience.reset()


# if __name__ == "__main__":
#     infer = Infer()

#     infer.infer(state)
