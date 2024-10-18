#include <asm/unistd.h>
#include <linux/perf_event.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <unistd.h>

#include <chrono>
#include <iostream>
#include <fstream>
#include <sstream>

#include "cpucounters.h"
#include "perfmon/pfmlib.h"

enum EventDomain : uint8_t {
  USER = 0b1,
  KERNEL = 0b10,
  HYPERVISOR = 0b100,
  ALL = 0b111
};
const int CPU_CORES = 24;

// Only measure the memory BW of socket 0.
const int socket = 0;

using namespace std;

long perf_event_open(struct perf_event_attr* hw_event, pid_t pid, int cpu,
  int group_fd, unsigned long flags) {
  int ret;

  ret = syscall(__NR_perf_event_open, hw_event, pid, cpu, group_fd, flags);
  return ret;
}

std::string metrics_log(string log_dir, uint32_t count) {
    return log_dir + "/metrics.log." + std::to_string(count);
}

void printReport(std::chrono::time_point<std::chrono::steady_clock> startTime,
  std::chrono::time_point<std::chrono::steady_clock> stopTime,
  pcm::SocketCounterState beforeState,
  pcm::SocketCounterState afterState, string log_dir, uint32_t count) {
  // void printReport(std::chrono::time_point<std::chrono::steady_clock> startTime,
  //   std::chrono::time_point<std::chrono::steady_clock> stopTime,
  //   pcm::SocketCounterState beforeState,
  //   pcm::SocketCounterState afterState, long long instructions,
  //   long long cycles) {
  auto duration = stopTime - startTime;
  auto elapsedMicros =
    std::chrono::duration_cast<std::chrono::microseconds>(duration).count();
  auto elapsedSeconds =
    std::chrono::duration_cast<std::chrono::seconds>(duration).count();
  auto bytesWrittenToPMM = pcm::getBytesWrittenToPMM(beforeState, afterState);
  auto bytesReadFromPMM = pcm::getBytesReadFromPMM(beforeState, afterState);
  auto bytesReadFromMC = pcm::getBytesReadFromMC(beforeState, afterState);
  auto bytesWrittenToMC = pcm::getBytesWrittenToMC(beforeState, afterState);
  auto instructions = pcm::getInstructionsRetired(beforeState, afterState);
  auto cycles = pcm::getCycles(beforeState, afterState);
  auto ipc = pcm::getIPC(beforeState, afterState);
  double ipus = static_cast<double>(instructions) / elapsedMicros;
  double writtenToPmmMBPerSec =
    static_cast<double>(bytesWrittenToPMM) / elapsedMicros;
  double readFromPmmMBPerSec =
    static_cast<double>(bytesReadFromPMM) / elapsedMicros;
  double writtenToDramMCMBPerSec =
    static_cast<double>(bytesWrittenToMC) / elapsedMicros;
  double readFromDramMCMBPerSec =
    static_cast<double>(bytesReadFromMC) / elapsedMicros;
  pcm::uint64 l3CacheMisses = pcm::getL3CacheMisses(beforeState, afterState);
  pcm::uint64 l2CacheMisses = pcm::getL2CacheMisses(beforeState, afterState);
  double l3CacheHitRatio = pcm::getL3CacheHitRatio(beforeState, afterState);
  double l2CacheHitRatio = pcm::getL2CacheHitRatio(beforeState, afterState);
  double llcReadMissLatency =
    pcm::getLLCReadMissLatency(beforeState, afterState);
  double l3CacheMissesPerUS =
    static_cast<double>(l3CacheMisses) / elapsedMicros;
  double l2CacheMissesPerUS =
    static_cast<double>(l2CacheMisses) / elapsedMicros;

  std::stringstream ss;

  ss << std::fixed << std::setprecision(4);
  ss << "ExecutionTime: " << elapsedSeconds << " seconds" << endl;
  ss << "IPC: " << ipc << endl;
  ss << "IPUS: " << ipus << " /us" << endl;
  ss << "Instructions: " << instructions << endl;
  ss << "Cycles: " << cycles << endl;
  ss << "WrittenToPMM: " << writtenToPmmMBPerSec << " MB/s" << endl;
  ss << "ReadFromPMM: " << readFromPmmMBPerSec << " MB/s" << endl;
  ss << "WrittenToDRAM: " << writtenToDramMCMBPerSec << " MB/s" << endl;
  ss << "ReadFromDRAM: " << readFromDramMCMBPerSec << " MB/s" << endl;
  ss << "L2CacheMisses: " << l2CacheMissesPerUS << " /us" << endl;
  ss << "L3CacheMisses: " << l3CacheMissesPerUS << " /us" << endl;
  ss << "L2CacheHitRatio: " << l2CacheHitRatio << endl;
  ss << "L3CacheHitRatio: " << l3CacheHitRatio << endl;
  ss << "LLCReadMissLatency: " << llcReadMissLatency << endl;

  std::ofstream logFile(metrics_log(log_dir, count));
  if (logFile.is_open()) {
      logFile << ss.str();
      logFile.close();
  } else {
      std::cerr << "Unable to open log file";
      exit(EXIT_FAILURE);
  }
}

void start_counter(int fd) {
  if (ioctl(fd, PERF_EVENT_IOC_RESET, 0) == -1) {
    perror("ioctl(PERF_EVENT_IOC_RESET)");
    exit(EXIT_FAILURE);
  }
  if (ioctl(fd, PERF_EVENT_IOC_ENABLE, 0) == -1) {
    perror("ioctl(PERF_EVENT_IOC_ENABLE)");
    exit(EXIT_FAILURE);
  }
}

void read_counter(const string& name, int fd, long long* value) {
  auto s = read(fd, value, sizeof(long long));
  if (s != sizeof(long long)) {
    std::ostringstream oss;
    oss << "Error reading counter " << name << " ,size: " << s
      << " ,value: " << *value;
    perror(oss.str().c_str());
    exit(EXIT_FAILURE);
  }
  cerr << "Counter: " << name << " value: " << *value << endl;
}

void stop_counter(int fd) { ioctl(fd, PERF_EVENT_IOC_DISABLE, 0); }

bool is_process_running(pid_t pid) {
  return (kill(pid, 0) == 0);
}

void wait_workload(pid_t workload_pid, uint32_t collect_period) {
  auto start = std::chrono::steady_clock::now();
  while (1) {
    if (is_process_running(workload_pid)) {
      if (collect_period > 0) {
        auto now = std::chrono::steady_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::seconds>(now - start);
        if (duration.count() >= collect_period) {
          cout << "Collect period finished" << endl;
          break;
        }
      }
      std::this_thread::sleep_for(std::chrono::milliseconds(500));
    }
    else {
      cout << "Application finished" << endl;
      break;
    }
  }
}

void start_counters_for_all_fds(const std::vector<long>& fds) {
  for (long fd : fds) {
    start_counter(fd);
  }
}

void stop_counters_for_all_fds(const std::vector<long>& fds) {
  for (long fd : fds) {
    stop_counter(fd);
  }
}

long long read_and_sum_counters(const std::string& name, const std::vector<long>& fds) {
  long long total = 0;
  for (long fd : fds) {
    long long count;
    read_counter(name, fd, &count);
    total += count;
  }
  return total;
}

std::vector<long> register_counter_for_all_cpus(const std::string& name, int workload_pid, uint64_t type,
  uint64_t eventID, EventDomain domain) {
  struct perf_event_attr pe;
  memset(&pe, 0, sizeof(struct perf_event_attr));
  pe.type = static_cast<uint32_t>(type);
  pe.size = sizeof(struct perf_event_attr);
  pe.config = eventID;
  pe.disabled = 1;
  pe.inherit = 1;
  pe.inherit_stat = 1;
  pe.exclude_user = !(domain & EventDomain::USER);
  pe.exclude_kernel = !(domain & EventDomain::KERNEL);
  pe.exclude_hv = !(domain & EventDomain::HYPERVISOR);

  std::vector<long> fds;
  for (int cpu = 0; cpu < CPU_CORES; ++cpu) {
    long fd = perf_event_open(&pe, workload_pid, cpu, -1, 0);
    std::cerr << "perf_event_open " << name << " fd is: " << fd << std::endl;
    if (fd == -1) {
      perror(("perf_event_open " + name).c_str());
      exit(EXIT_FAILURE);
    }
    fds.push_back(fd);
  }
  return fds;
}

// start perf event for period collection
long register_counter(const string& name, int workload_pid, uint64_t type,
  uint64_t eventID, EventDomain domain) {
  struct perf_event_attr pe;
  memset(&pe, 0, sizeof(struct perf_event_attr));
  pe.type = static_cast<uint32_t>(type);
  pe.size = sizeof(struct perf_event_attr);
  pe.config = eventID;
  pe.disabled = 1;
  pe.inherit = 1;
  pe.inherit_stat = 1;
  pe.exclude_user = !(domain & EventDomain::USER);
  pe.exclude_kernel = !(domain & EventDomain::KERNEL);
  pe.exclude_hv = !(domain & EventDomain::HYPERVISOR);
  // pe.read_format =
  //     PERF_FORMAT_TOTAL_TIME_ENABLED | PERF_FORMAT_TOTAL_TIME_RUNNING;

  long fd = perf_event_open(&pe, workload_pid, -1, -1, 0);
  cerr << "perf_event_open " << name << " fd is: " << fd << endl;
  if (fd == -1) {
    perror(("perf_event_open " + name).c_str());
    exit(EXIT_FAILURE);
  }
  return fd;
}

pcm::PCM* init_pcm() {
  pcm::PCM* pcm = pcm::PCM::getInstance();
  pcm->resetPMU();
  pcm::PCM::ErrorCode status = pcm->program();
  if (status != pcm::PCM::Success) {
    cerr << "Failed to initialize PCM: " << status << endl;
    exit(EXIT_FAILURE);
  }
  return pcm;
}

void collect_metrics(pid_t workload_pid, uint32_t collect_period, pid_t pebs_target_pid, string log_dir) {
  int ret = pfm_initialize();
  if (ret != PFM_SUCCESS) {
    cerr << "Cannot initialize library: " << pfm_strerror(ret) << endl;
    exit(EXIT_FAILURE);
  }
  //   std::vector<long> fd1_vec;
  //   std::vector<long> fd2_vec;
  //   long fd1;
  //   long fd2;
  //   if (pebs_target_pid == -1) {
  //     fd1_vec = register_counter_for_all_cpus("instructions", pebs_target_pid, PERF_TYPE_HARDWARE,
  //       PERF_COUNT_HW_INSTRUCTIONS, EventDomain::USER);
  //     fd2_vec = register_counter_for_all_cpus("cycles", pebs_target_pid, PERF_TYPE_HARDWARE,
  //       PERF_COUNT_HW_CPU_CYCLES, EventDomain::USER);
  //     start_counters_for_all_fds(fd1_vec);
  //     start_counters_for_all_fds(fd2_vec);
  //   }
  //   else {
  //     fd1 = register_counter("instructions", pebs_target_pid, PERF_TYPE_HARDWARE,
  //       PERF_COUNT_HW_INSTRUCTIONS, EventDomain::USER);
  //     fd2 = register_counter("cycles", pebs_target_pid, PERF_TYPE_HARDWARE,
  //       PERF_COUNT_HW_CPU_CYCLES, EventDomain::USER);
  //     start_counter(fd1);
  //     start_counter(fd2);
  //   }

  pcm::PCM* pcm = init_pcm();
  uint32_t count = 0;
  while (true) {
    if (!is_process_running(workload_pid)) {
      break;
    }
    count++;
    pcm::SocketCounterState beforeState = pcm->getSocketCounterState(socket);
    auto startTime = std::chrono::steady_clock::now();

    wait_workload(workload_pid, collect_period);

    auto stopTime = std::chrono::steady_clock::now();
    pcm::SocketCounterState afterState = pcm->getSocketCounterState(socket);

    printReport(startTime, stopTime, beforeState, afterState, log_dir, count);
  }

  // pcm::SocketCounterState beforeState = pcm->getSocketCounterState(socket);
  // auto startTime = std::chrono::steady_clock::now();


  // wait_workload(workload_pid, collect_period);

  // auto stopTime = std::chrono::steady_clock::now();
  // pcm::SocketCounterState afterState = pcm->getSocketCounterState(socket);

  // //   long long instructions = 0;
  // //   long long cycles = 0;
  // //   if (pebs_target_pid == -1) {
  // //     stop_counters_for_all_fds(fd1_vec);
  // //     stop_counters_for_all_fds(fd2_vec);
  // //     instructions = read_and_sum_counters("instructions", fd1_vec);
  // //     cycles = read_and_sum_counters("cycles", fd2_vec);
  // //   }
  // //   else {
  // //     stop_counter(fd1);
  // //     stop_counter(fd2);
  // //     read_counter("instructions", fd1, &instructions);
  // //     read_counter("cycles", fd2, &cycles);
  // //     close(fd1);
  // //     close(fd2);
  // //   }

  // // printReport(startTime, stopTime, beforeState, afterState, instructions, cycles);
  // printReport(startTime, stopTime, beforeState, afterState, log_dir, count);
}

void exec_shell_cmd(char* cmd)
{
  FILE* fp;
  char bp[500];
  fp = popen(cmd, "r");
  while (fgets(bp, sizeof(bp), fp) != NULL) {
    printf("%s", bp);
  }
  pclose(fp);
}

int main(int argc, char* argv[]) {
  pid_t pid = getpid();
  printf("Pid of collector is %d\n", pid);
  char cmd[256];
  sprintf(cmd, "choom --adjust -1000 -p %d", (int)pid);
  exec_shell_cmd(cmd);

  if (argc < 6) {
    cerr << "Usage: " << argv[0] << " <warmup_seconds>" << " <workload_pid>" << " <collect_period>" << " <pebs_target_pid>" << " <log_dir>" << endl;
    exit(EXIT_FAILURE);
  }
  uint32_t warmup_seconds = atoi(argv[1]);
  cerr << "Warmup seconds: " << warmup_seconds << endl;
  pid_t workload_pid = atoi(argv[2]);
  cerr << "Workload pid: " << workload_pid << endl;
  sleep(warmup_seconds);

  uint32_t collect_period = 0;
  collect_period = atoi(argv[3]);
  cerr << "Collect period: " << collect_period << endl;
  pid_t pebs_target_pid = atoi(argv[4]);
  cerr << "PEBS target pid: " << pebs_target_pid << endl;
  string log_dir = argv[5];
  cerr << "Log dir: " << log_dir << endl;
  collect_metrics(workload_pid, collect_period, pebs_target_pid, log_dir);
  return 0;
}
