import subprocess
import sys
import os

command = sys.argv[1:]

print(f"start_workload command: {command}")
process = subprocess.Popen(command)
pid = process.pid

subprocess.Popen(f"sudo choom --adjust -1000 -p {pid}", shell=True)
pid_file = f"{os.environ['LOG_DIR']}/workload.pid"
print(f"Writing PID to {pid_file}")
with open(pid_file, 'w') as file:
    file.write(str(pid))

print(f"Workload PID: {pid}")

process.wait()  # Wait for the process to finish
