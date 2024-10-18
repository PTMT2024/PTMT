#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <err.h>
#include <sys/wait.h>

int syscall_htmm_start = 449;
int syscall_htmm_end = 450;

long htmm_start(pid_t pid, int node)
{
    return syscall(syscall_htmm_start, pid, node);
}

long htmm_end(pid_t pid)
{
    return syscall(syscall_htmm_end, pid);
}

void write_pid_to_file(pid_t pid)
{
    FILE *file;
    char *log_dir = getenv("LOG_DIR");
    char pid_file[256];

    sprintf(pid_file, "%s/workload.pid", log_dir);

    file = fopen(pid_file, "w");
    if (file == NULL) {
        perror("Unable to open file");
        exit(1);
    }

    fprintf(file, "%d", pid);
    fclose(file);
}

int main(int argc, char** argv)
{
    printf("start ");
#ifdef __NOPID
    printf("launch_bench_nopid\n");
#else
    printf("launch_bench\n");
#endif
    pid_t pid;
    int state;

    if (argc < 2) {
	    printf("Usage ./launch_bench [BENCHMARK]");	
	    htmm_end(-1);
	    return 0;
    }
    printf("Forking\n");
    pid = fork();
    if (pid == 0) {
	    execvp(argv[1], &argv[1]);
	    perror("Fails to run bench");
	    exit(-1);
    }
    write_pid_to_file(pid);
#ifdef __NOPID
    printf("htmm_start(-1, 0)\n");
    htmm_start(-1, 0);
#else
    printf("htmm_start(%d, 0)\n", pid);
    htmm_start(pid, 0);
#endif
    printf("pid: %d\n", pid);
    waitpid(pid, &state, 0);

    htmm_end(-1);
    
    return 0;
}