import subprocess
import os
import time
import signal
import sys
from var import *
import logging
import coloredlogs
import re

from datetime import datetime


coloredlogs.install()
logging.basicConfig(
    format = '%(asctime)s [%(module)s:%(funcName)s]:%(levelname)s: %(message)s',
    datefmt = '%Y/%m/%d %H:%M:%S',
    level = logging.INFO
)

class Timer:
    """Timer used for an experiment"""

    def __init__ (self):
        pass


    def start (self):
        """Start timer"""

        self.start_t = datetime.now()


    def end (self):
        """End timer"""

        self.end_t = datetime.now()


    def print (self):
        """Print elapsed time"""

        self.delta_t = self.end_t - self.start_t
        logging.info(f"Elapsed time: {self.delta_t}\n")


def kill_processes_by_pid(pid):
    try:
        print(f"Try to kill pid {pid}")
        subprocess.run([f"kill {pid}"],shell=True, text=True, check=True)
        print(f"Killed pid {pid}")
    except subprocess.CalledProcessError:
        print(f"No processes found matching: {pid}")

def kill_processes_by_pattern(pattern):
    try:
        command = f"pgrep -f '{pattern}'"
        output = subprocess.check_output(command, shell=True, text=True)
        process_ids = output.strip().split("\n")
        print(f"{pattern} pids: {process_ids}")
        for pid in process_ids:
            subprocess.run(["kill", pid])
            print(f"Killed pid {pid}")
    except subprocess.CalledProcessError:
        print(f"No processes found matching: {pattern}")


def get_pid_of_process(workload):
    try:
        command = f"ps aux --sort=-pcpu | grep '{workload}' | grep -v grep"
        output = subprocess.check_output(command, shell=True, text=True)
        workload_pid = int(output.strip().split("\n")[0].split()[1])
        return workload_pid
    except subprocess.CalledProcessError:
        print(f"No pid found for {workload}")
        return None


def get_numa_free_memory():
    try:
        output = subprocess.check_output("numactl --hardware", shell=True, text=True)
        print(output)
        lines = output.split("\n")
        node_free_size = {}
        for line in lines:
            if "node" in line and "free" in line:
                parts = line.split()
                node = int(parts[1])
                size = int(parts[3])
                node_free_size[node] = size
        return node_free_size
    except subprocess.CalledProcessError:
        print("Error executing numactl")
        return None

def start_workload_cmd(mm, bench, workload_log, workload):
    print("workload: ", workload)
    cmd = ""
    if mm != "memtis":
         cmd = f"/usr/bin/time -f 'execution time %e (s)' numactl -N 0 -- {PythonExe} {MLDPP_DIR}/mldpp/start_workload.py {bench} 2>&1 | stdbuf -oL -eL tee {workload_log}"
    else:
        cmd =  f"/usr/bin/time -f 'execution time %e (s)' numactl -N 0 -- {MLDPP_DIR}/run_scripts/scripts/memtis/bin/launch_bench_nopid {bench} 2>&1 | stdbuf -oL -eL tee {workload_log}"
        # if workload == 'Silo':
        #     cmd =  f"/usr/bin/time -f 'execution time %e (s)' {MLDPP_DIR}/run_scripts/scripts/memtis/bin/launch_bench_nopid {bench} 2>&1 | tee {workload_log}"
        # else:
        #     cmd = f"/usr/bin/time -f 'execution time %e (s)' {MLDPP_DIR}/run_scripts/scripts/memtis/bin/launch_bench {bench} 2>&1 | tee {workload_log}"
    print("start_workload_cmd: ", cmd)
    return cmd

def wait_workload(workload_pid, collect_period):
    if workload_pid == 0 and collect_period == 0:
        print("workload_pid and collect_period cannot be both 0. Exit")
        exit(1)

    start_time = time.time()

    while True:
        if workload_pid != 0:
            try:
                os.kill(workload_pid, 0)
            except OSError:
                print(f"Process {workload_pid} has finished.")
                time.sleep(2)
                break

        if collect_period > 0 and (time.time() - start_time >= collect_period):
            # print(f"Collect period of {collect_period} seconds has been reached.")
            break

        time.sleep(1)

def reliable_cat(file_path):
    output = ""
    for attempt in range(3):
        try:
            output = subprocess.check_output(
                f"cat {file_path}", shell=True, text=True
            )
            break  # If the command succeeds, break out of the loop
        except subprocess.CalledProcessError:
            if attempt < 2:  # only try for 3 times
                time.sleep(1)
            else:
                sys.exit("Exiting after 3 failed attempts")
    return output