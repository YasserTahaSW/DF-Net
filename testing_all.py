import sys
import subprocess
import glob
import os
sys.path.append('/system/user/taha/pycharmprojects/DF-Net-master/kitti_eval/')


def read_results():
    results =[]
    with open("test.log", 'r') as f:
        [results.append(float(line.strip('\n\r'))) for line in f]
    return results

def compute_cmd(cmd):
    try:
        p = subprocess.Popen(
            cmd,
            stdout = subprocess.PIPE)
        p.wait()
    except subprocess.CalledProcessError as e:
        print("common::run_command() : [ERROR]: output = %s, error code = %s\n"
              % (e.output, e.returncode))


def get_latest_checkpoint():
    list_of_files = glob.glob('/system/user/taha/pycharmprojects/DF-Net-master/out/mod*') # * means all if need specific format then *.csv
    if len(list_of_files):
        latest_file = max(list_of_files, key=os.path.getctime)
        latest_file = os.path.splitext(latest_file)[0]
        return latest_file
    else:
        return 0

def main():

    latest_file = get_latest_checkpoint()

    if latest_file:
        # testing flow
        test_flow12 = "/system/user/taha/pycharmprojects/DF-Net-master/test_flownet_2012.py"
        arg1_12 = "--dataset_dir=/publicdata/kitti/optical_flow_2012/testing/"
        arg2_12 = "--ckpt_file=" + latest_file
        arg3_12 = '--output_dir=/system/user/taha/pycharmprojects/DF-Net-master/out'

        # testing flow
        test_flow15 = "/system/user/taha/pycharmprojects/DF-Net-master/test_flownet_2015.py"
        arg1_15 = "--dataset_dir=/publicdata/kitti/optical_flow_2015/testing/"
        arg2_15 = "--ckpt_file=" + latest_file

        # testing depth
        test_depth = '/system/user/taha/pycharmprojects/DF-Net-master/test_kitti_depth.py'
        arg_d1 = '--dataset_dir=/publicdata/kitti/kitti_rawdata/'
        arg_d2 = '--output_dir=/system/user/taha/pycharmprojects/DF-Net-master/out'
        arg_d3 = '--ckpt_file=' + latest_file
        arg_d4 = '--split=val'

        # evaluating depth
        eval_depth = '/system/user/taha/pycharmprojects/DF-Net-master/kitti_eval/eval_depth.py'
        arg_ed1 = '--pred_file=' + latest_file + ".npy"
        arg_ed2 = arg_d4
        arg_ed3 = '--kitti_dir=/publicdata/kitti/kitti_rawdata/'

        args_f12 = ['python', test_flow12, arg1_12, arg2_12, arg3_12]
        args_f15 = ['python', test_flow15, arg1_15, arg2_15]
        args_comp_depth = ['python', test_depth, arg_d1, arg_d2, arg_d3, arg_d4]
        args_eval_deth = ['python', eval_depth, arg_ed1, arg_ed2, arg_ed3]

        compute_cmd(args_f12)
        results_flow12 = read_results()
        compute_cmd(args_f15)
        results_flow15 = read_results()
        compute_cmd(args_comp_depth)
        compute_cmd(args_eval_deth)
        results_depth = read_results()


        print("results of test flow12 is:", results_flow12)
        print("results of test flow15 is:", results_flow15)
        print("results of test depth is:", results_depth)

        return [results_flow12, results_flow15, results_depth]
    else:
        return 0

if __name__ == '__main__':
    main()