#!/bin/bash

export DIR=/home/sherry/projects/sk_prokect/mldpp/run_scripts
export PyDIR=/home/sherry/projects/sk_prokect/mldpp/mldpp
export WORKLOAD_SOCKET=0
export TUNING_SOCKET=1

function func_cache_flush() {
	echo 3 | sudo tee /proc/sys/vm/drop_caches                            # Clear caches to maximize available RAM
	echo 1 | sudo tee /proc/sys/vm/compact_memory                         # Rearrange RAM usage to maximise the size of free blocks

    free
    return
}

function func_prepare() {
    echo "Preparing benchmark start..."


	echo never | sudo tee /sys/kernel/mm/transparent_hugepage/enabled
	echo never | sudo tee /sys/kernel/mm/transparent_hugepage/defrag

	sudo sysctl kernel.perf_event_max_sample_rate=100000

	export OMP_NUM_THREADS=24
	# export PythonExe = "/usr/bin/python3"

	if [[ "x${TYPE}" == "xidt_train" ]]; then
		export PythonExe="/home/sherry/miniconda3/envs/IDT/bin/python"
	elif [[ "x${TYPE}" == "xidt_tune" ]]; then
		export PythonExe="/home/sherry/miniconda3/envs/IDT/bin/python"
	else
		export PythonExe="/home/sherry/miniconda3/envs/RL/bin/python"
	fi 
	sudo pkill -f mldpp_metrics_collector
	sudo pkill -f user_space_page_migration
	sudo killall -9 vmstat.sh
	sudo killall -9 memusage.sh

	if [[ -e ${DIR}/bench_cmds/${BENCH_NAME}.sh ]]; then
	    source ${DIR}/bench_cmds/${BENCH_NAME}.sh
	else
	    echo "ERROR: ${BENCH_NAME}.sh does not exist."
	    exit -1
	fi

    export LOG_DIR=${DIR}/log/${TYPE}/${MM}/${COLLECT_PERIOD}s/${BENCH_NAME}/${CURRENT_DATE}_${LOCAL_MEM}_${WORKLOAD_SOCKET}_${TUNING_SOCKET}
    mkdir -p ${LOG_DIR}

    if [[ -e ${DIR}/config_settings/${MM}.sh ]]; then
	    source ${DIR}/config_settings/${MM}.sh
	else
	    echo "ERROR: ${MM}.sh does not exist."
	    exit -1
	fi
	func_cache_flush

	sleep 15
}

function func_usage() {
    echo
    echo -e "Usage: $0 [-B benchmark] [-MM memmanagement] [-LM localmem]..."
    echo
    echo "  -T,   --type   			[arg]   operation type to run. e.g., collect, tune, etc"
    echo "  -B,   --benchmark   	[arg]   benchmark name to run. e.g., Graph500, XSBench, etc"
    echo "  -MM,  --memmanagement  	[arg]   memmanagement to run. e.g., autonuma, TPP, etc"
	echo "  -LM,  --localmem    	[arg]   local memory size. e.g., 65G, 105G, etc"
    echo "  -?,   --help"
    echo "        --usage"
    echo
}

# get options:
while (( "$#" )); do
    case "$1" in
	-T|--type)
	    if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
		TYPE=( "$2" )
		shift 2
	    else
		echo "Error: Argument for $1 is missing" >&2
		func_usage
		exit -1
	    fi
	    ;;
	-B|--benchmark)
	    if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
		BENCH_NAME=( "$2" )
		shift 2
	    else
		echo "Error: Argument for $1 is missing" >&2
		func_usage
		exit -1
	    fi
	    ;;
	-MM|--memmanagement)
	    if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
		MM=( "$2" )
		shift 2
	    else
		echo "Error: Argument for $1 is missing" >&2
		func_usage
		exit -1
	    fi
	    ;;
	-LM|--localmem)
	    if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
		LOCAL_MEM=( "$2" )
		shift 2
	    else
		echo "Error: Argument for $1 is missing" >&2
		func_usage
		exit -1
	    fi
	    ;;
	-CP|--collectperiod)
		if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
		COLLECT_PERIOD=( "$2" )
		shift 2
	    else
		echo "Error: Argument for $1 is missing" >&2
		func_usage
		exit -1
	    fi
	    ;;
	-H|-?|-h|--help|--usage)
	    func_usage
	    exit
	    ;;
	*)
	    echo "Error: Invalid option $1"
	    func_usage
	    exit -1
	    ;;
    esac
done

function func_main() {
    TIME="/usr/bin/time"

    cat /proc/vmstat | grep -e thp -e htmm -e migrate -e pgpromote -e pgdemote -e numa -e promote> ${LOG_DIR}/before_vmstat.log 
    if [[ "x${TYPE}" == "xidt_train" ]]; then
			mv ${PyDIR}/idt/pre-trained.${MM}/checkpoint.old ${PyDIR}/idt/pre-trained.${MM}/checkpoint.old.old
            mv ${PyDIR}/idt/pre-trained.${MM}/checkpoint ${PyDIR}/idt/pre-trained.${MM}/checkpoint.old
            cp -r -f ${PyDIR}/idt/chkpt.${MM}/* ${PyDIR}/idt/pre-trained.${MM}/checkpoint
			if [ $? -ne 0 ]; then
    			echo "Error occurred during copy. Restoring backup..."
    			mv ${PyDIR}/idt/pre-trained.${MM}/checkpoint.old ${PyDIR}/idt/pre-trained.${MM}/checkpoint
				mv ${PyDIR}/idt/pre-trained.${MM}/checkpoint.old.old ${PyDIR}/idt/pre-trained.${MM}/checkpoint.old
			else
				rm -r -f ${PyDIR}/idt/pre-trained.${MM}/checkpoint.old.old
			fi
	fi
    ${DIR}/scripts/vmstat.sh ${LOG_DIR} &
    ${DIR}/scripts/memusage.sh ${LOG_DIR} &

	if [[ "x${MM}" == "xmemtis" ]]; then
	${DIR}/scripts/memtis/bin/kill_ksampled
	# set memcg for htmm
    sudo ${DIR}/scripts/memtis/set_htmm_memcg.sh htmm remove
    sudo ${DIR}/scripts/memtis/set_htmm_memcg.sh htmm $$ enable
    sudo ${DIR}/scripts/memtis/set_mem_size.sh htmm 0 ${LOCAL_MEM}
    sleep 2
	# numactl -C 0-23 -- sudo ${PythonExe} ${PyDIR}/mldpp.py ${TYPE} -W ${BENCH_NAME} -M ${MM} -B "${BENCH_RUN}" -L ${LOG_DIR} -P ${COLLECT_PERIOD} 2>&1 | tee ${LOG_DIR}/mldpp.log
	sudo -E ${PythonExe} ${PyDIR}/mldpp.py ${TYPE} -W ${BENCH_NAME} -M ${MM} -B "${BENCH_RUN}" -L ${LOG_DIR} -P ${COLLECT_PERIOD}
	elif [[ "x${MM}" == "xtpp" ]]; then
	# numactl -C 0-23 -m 0,2 -- sudo -E ${PythonExe} ${PyDIR}/mldpp.py ${TYPE} -W ${BENCH_NAME} -M ${MM} -B "${BENCH_RUN}" -L ${LOG_DIR} -P ${COLLECT_PERIOD}  2>&1 | tee ${LOG_DIR}/mldpp.log
	numactl -N ${TUNING_SOCKET} -- sudo -E ${PythonExe} ${PyDIR}/mldpp.py ${TYPE} -W ${BENCH_NAME} -M ${MM} -B "${BENCH_RUN}" -L ${LOG_DIR} -P ${COLLECT_PERIOD}  2>&1 | tee ${LOG_DIR}/mldpp.log
	else
	numactl -N ${TUNING_SOCKET} -- sudo -E ${PythonExe} ${PyDIR}/mldpp.py ${TYPE} -W ${BENCH_NAME} -M ${MM} -B "${BENCH_RUN}" -L ${LOG_DIR} -P ${COLLECT_PERIOD} 2>&1 | tee ${LOG_DIR}/mldpp.log
	fi

    sudo killall -9 vmstat.sh
    sudo killall -9 memusage.sh
    cat /proc/vmstat | grep -e thp -e htmm -e migrate -e pgpromote -e pgdemote -e numa -e promote > ${LOG_DIR}/after_vmstat.log
    sudo dmesg -c > ${LOG_DIR}/dmesg.log

    sleep 5
    if [[ "x${BENCH_NAME}" == "xbtree" ]]; then
	cat ${LOG_DIR}/output.log | grep Throughput \
	    | awk ' NR%20==0 { print sum ; sum = 0 ; next} { sum+=$3 }' \
	    > ${LOG_DIR}/throughput.out
    elif [[ "x${BENCH_NAME}" =~ "xsilo" ]]; then
	cat ${LOG_DIR}/output.log | grep -e '0 throughput' -e '5 throughput' \
	    | awk ' { print $4 }' > ${LOG_DIR}/throughput.out
    fi
	
	sudo pkill -f mldpp_metrics_collector
	sudo pkill -f user_space_page_migration
	sudo pkill -f "${BENCH_RUN}"
	if [[ "x${MM}" == "xmemtis" ]]; then
	sudo ${DIR}/scripts/memtis/set_htmm_memcg.sh htmm $$ disable
	fi

}

func_prepare
func_main
