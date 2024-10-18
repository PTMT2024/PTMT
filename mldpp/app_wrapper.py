#!/usr/bin/env python

import sys
import subprocess
import os
import datetime
from time import sleep

def run_program(app_cmd):
    """
    This function will run a single instance of the app with given parameters in the background.
    """
    # Start the process without waiting for it to finish (non-blocking)
    process = subprocess.Popen(app_cmd, shell=True)
    
    # Return the process object to track it later
    return process

def main():
    if len(sys.argv) < 3:
        print("Usage: ./app_wrapper <num_copies> <app_cmd>")
        sys.exit(1)

    num_copies = int(sys.argv[1])
    app_cmd = " ".join(sys.argv[2:])

    processes = []

    print(f"Running: {app_cmd} with {num_copies} copies")
    start_time = datetime.datetime.now()

    # Run multiple instances of the program concurrently
    for i in range(num_copies):
        print(f"Launching instance {i+1}/{num_copies}")
        process = run_program(app_cmd)
        processes.append(process)
        sleep(1)

    # Wait for all processes to complete
    for i, process in enumerate(processes):
        process.wait()  # This will wait for each process to finish
        print(f"Instance {i+1}/{num_copies} finished.")
    
    end_time = datetime.datetime.now()
    total_execution_time = (end_time - start_time).total_seconds()
    print(f"Time: {total_execution_time} seconds")
    print("All instances finished.")

if __name__ == "__main__":
    main()
