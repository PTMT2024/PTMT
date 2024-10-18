
from idt.train import *
from idt.infer import *
from var import *

class IDTDriver:
    def __init__(self, memmanagement, collect_period, logdir, ldram_size, bench_pid):
        self.memmanagement = memmanagement
        self.logdir = logdir
        self.collect_period = collect_period
        self.ldram_size = ldram_size
        self.bench_pid = bench_pid
    
    def run_infer (self, itr, infer, n_infer, chkpt, timer):
        """
        Driver for running infer.

        :param infer: Infer class instance
        :param chkpt: checkpoint to be restored
        :param timer: Timer class instance
        """

        logging.info("Infer start.") 
        timer.start()
    
        infer.load_mdl_and_reset_experience(chkpt)
        terminated = False

        for i in range(n_infer):
            print(f"iter {itr} infer {i}")
            terminated = infer.infer()
            if terminated:
                return terminated

        Experience.write()
        Experience.reset()

        logging.info("Infer end.") 
        timer.end()
        timer.print()
        return terminated


    def run_train (self, train, timer):
        """
        Driver for running train.

        :param train: Train class instance
        :param timer: Timer class instance
        :return: saved checkpoint file
        """

        logging.info("Train start.")

        timer.start()
        chkpt = train.train()

        logging.info("Train end.")
        timer.end()
        timer.print()

        return chkpt


    def driver (self, n_iter):
        """
        Driver.

        Invoke this method to run.
        Infer and train is invoked repeatedly.

        :param n_iter: Number of iterations to be runned.
        """

        chkpt =  f"{MLDPP_DIR}/mldpp/idt/pre-trained.{self.memmanagement}/checkpoint"

        need_restore = True
        Action.__init__(self.memmanagement, self.bench_pid)
        idt_state = IDTState(self.logdir, self.ldram_size, self.memmanagement)
        infer = Infer(need_restore, self.memmanagement, self.bench_pid, self.collect_period, self.logdir, self.ldram_size, idt_state, chkpt)
        train = Train(need_restore, chkpt, self.memmanagement, self.collect_period, self.logdir, self.ldram_size, self.bench_pid)
        timer = Timer()

        #n_infer = 32
        n_infer = 4

        infer.reset()
        for itr in range(n_iter):
            terminated = self.run_infer(itr, infer, n_infer, chkpt, timer)
            if terminated:
                logging.info("workload terminated")
                break
            
            start_time = time.time()
            chkpt = self.run_train(train, timer)
            end_time = time.time()
            consuming_time_us = (end_time - start_time) * 1_000_000
            logging.info(f"Training time: {consuming_time_us:.2f} us")

        del train
        del infer
