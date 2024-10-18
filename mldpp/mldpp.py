import argparse
import sys
from knn_model import *
import importlib

def main():
    parser = argparse.ArgumentParser(description="MLDPP Script")
    parser.add_argument("action", choices=["collect", "tune", "defaulttune", "onedefaulttune", 'tune_ipc', 'onerandomtune', 'defaulttunewithml', 'notune', 'tune_v2', 'tune_v2_ipc', 'tune_dnn', 'tune_v2_ipc_no_tnorm', 'tune_ipc_no_tnorm', 'tune_rl', 'tune_rl_online', 'idt_train', 'idt_tune', 'knn_sensitivity_5', 'knn_sensitivity_10', 'knn_sensitivity_15', 'knn_sensitivity_20', 'knn_sensitivity_30', 'knn_sensitivity_35', 'knn_sensitivity_40', 'knn_sensitivity_45', 'knn_sensitivity_50', 'tune_rl_wo_pretrain'], help="Action to perform")
    parser.add_argument("-L", "--logdir",type=str, help="Log Dir")
    parser.add_argument("-B", "--bench", type=str, help="Benchmark command")
    parser.add_argument("-M", "--memmanagement", type=str, help="Memory management")
    parser.add_argument("-W", "--workload", type=str, help="Workload name")
    parser.add_argument("-P", "--collectperiod", type=str, help="CollectPeriod")
    args = parser.parse_args()
    workload = args.workload
    logdir = args.logdir
    bench = args.bench
    memmanagement = args.memmanagement
    collectperiod = args.collectperiod
    if args.action == "collect":
        tuner = importlib.import_module('collector')
        tuner.Collector(workload, memmanagement, bench, logdir, collectperiod).do()
    elif args.action == "tune":
        tuner = importlib.import_module('tuner')
        tuner.Tuner(workload, memmanagement, bench, logdir, collectperiod).do()
    elif args.action == "tune_v2":
        tuner = importlib.import_module('tuner_v2')
        tuner.TunerV2(workload, memmanagement, bench, logdir, collectperiod).do()
    elif args.action == "tune_v2_ipc":
        tuner = importlib.import_module('tuner_v2_ipc')
        tuner.TunerV2IPC(workload, memmanagement, bench, logdir, collectperiod).do()
    elif args.action == "tune_v2_ipc_no_tnorm":
        tuner = importlib.import_module('tuner_v2_ipc_no_tnorm')
        tuner.TunerV2IPCNoTNorm(workload, memmanagement, bench, logdir, collectperiod).do()
    elif args.action == "tune_ipc_no_tnorm":
        tuner = importlib.import_module('tuner_ipc_no_tnorm')
        tuner.TunerIPCNoTNorm(workload, memmanagement, bench, logdir, collectperiod).do()
    elif args.action == "tune_dnn":
        tuner = importlib.import_module('tuner_dnn')
        tuner.TunerDNN(workload, memmanagement, bench, logdir, collectperiod).do()
    elif args.action == "tune_rl":
        tuner = importlib.import_module('tune_rl')
        tuner.TunerRL(workload, memmanagement, bench, logdir, collectperiod).do()
    elif args.action == "tune_rl_online":
        tuner = importlib.import_module('tune_rl_online')
        tuner.TunerRLOnline(workload, memmanagement, bench, logdir, collectperiod).do()
    elif args.action == "idt_train":
        tuner = importlib.import_module('idt_train')
        tuner.IDTTrainer(workload, memmanagement, bench, logdir, collectperiod).do()
    elif args.action == "idt_tune":
        tuner = importlib.import_module('idt_tune')
        tuner.IDTTuner(workload, memmanagement, bench, logdir, collectperiod).do()
    elif args.action == "defaulttune":
        tuner = importlib.import_module('default_tune')
        tuner.DefaultTuner(workload, memmanagement, bench, logdir, collectperiod).do()
    elif args.action == "defaulttunewithml":
        tuner = importlib.import_module('default_tune_with_ml')
        tuner.DefaultTunerWithML(workload, memmanagement, bench, logdir, collectperiod).do()
    elif args.action == "onedefaulttune":
        tuner = importlib.import_module('one_default_tune')
        tuner.OneDefaultTuner(workload, memmanagement, bench, logdir, collectperiod).do()
    elif args.action == "onerandomtune":
        tuner = importlib.import_module('one_random_tune')
        tuner.OneRandomTuner(workload, memmanagement, bench, logdir, collectperiod).do()
    elif args.action == "tune_ipc":
        tuner = importlib.import_module('tuner_ipc')
        tuner.TunerIPC(workload, memmanagement, bench, logdir, collectperiod).do()
    elif args.action == "notune":
        tuner = importlib.import_module('notune')
        tuner.NoTuner(workload, memmanagement, bench, logdir, collectperiod).do()
    elif args.action.startswith("knn_sensitivity_"):
        k_value = int(args.action.split("_")[-1])
        tuner = importlib.import_module('tune_knn_sensitivity')
        tuner.TunerKnnSensitivity(workload, memmanagement, bench, logdir, collectperiod, k_value).do()
    elif args.action == "tune_rl_wo_pretrain":
        tuner = importlib.import_module('tune_rl_wo_pretrain')
        tuner.TunerRLWOPretrain(workload, memmanagement, bench, logdir, collectperiod).do()
    
    else:
        print("Invalid action")
        sys.exit(1)

if __name__ == "__main__":
    main()
