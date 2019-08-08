#!/usr/bin/env python
import pdb
#pdb.set_trace()
import glob
from argparse import ArgumentParser
import os
from subprocess import Popen
from multiprocessing import Pool,cpu_count,active_children,Manager
import time
from subprocess import Popen

parser = ArgumentParser(description="Run splitting fastq by barcode by multithreads:")
parser.add_argument('--out_dir','-o', help="output folder")
parser.add_argument('--out_dir_prefix','-o_dir', help="Directory to store outputs")
parser.add_argument('--fastq_file','-f', help="origin fastq file")
parser.add_argument('--h5_dir','-h_dir', help="Directory to store h5 files")
parser.add_argument('--sample_name','-s', help="sample name")
parser.add_argument('--num_threads','-t',type=int,help="number of threads", default=3)
parser.add_argument('--chr_start','-start',type=int,help="chr start", default=1)
parser.add_argument('--chr_end','-end',type=int,help="chr end", default=23)
args = parser.parse_args()
script_path = os.path.dirname(os.path.abspath( __file__ ))

code_path = script_path + "/" 


def Run_split(cmd_used,xin):
    Popen(cmd_used,shell=True).wait()


def Run_all_chunks(out_dir,out_dir_prefix,h5_dir,sample_name,num_of_threads,chr_start,chr_end):
    fastq_files_all = sorted(glob.glob(out_dir +  "barcoded.fastq_part*"), key=os.path.getmtime)
    count = 1
    total_num = len(fastq_files_all)
    file_name_list = []
    pool = Pool(processes=num_of_threads)
    for one_file in fastq_files_all:
        use_prefix = one_file[len(out_dir+ "barcoded.fastq_part"):]
        out_dir_2 = out_dir + out_dir_prefix  + use_prefix + "/"
        if not(os.path.exists(out_dir_2)):
            os.makedirs(out_dir_2)
        cmd_used = "python3 " + code_path + "Split_barcoded_fastq_by_chr_all_by_smallchunks.py --chr_start " + str(chr_start) + " --chr_end " + str(chr_end) + " --out_dir " + out_dir_2 + " --fastq_file " + one_file + " --h5_dir " + h5_dir + " --sample_name " + sample_name  
        pool.apply_async(Run_split,(cmd_used, "xin"))
        count += 1
        file_name_list.append(one_file)
        if (count - 1)%num_of_threads == 0 or (count - 1) == total_num:
            pool.close()
            while len(active_children()) > 1:
                time.sleep(0.5)
            pool.join()
            for _file in file_name_list:
                Popen("rm " + _file,shell=True).wait()
                print(_file)
            file_name_list = []
            if (count - 1) == total_num:
                print("finish all")
            else:
                pool = Pool(processes=num_of_threads)
            
    print("All Done~")


def Concatenate_all(out_dir,out_dir_prefix,chr_start,chr_end):
    fastq_folder_all = sorted(glob.glob(out_dir +  out_dir_prefix + "*"), key=os.path.getmtime)
    for one_folder in fastq_folder_all:
        for chr_num in range(chr_start,chr_end + 1):
            use_cmd = "cat " + one_folder + "/" + "fastq_by_Chr_" + str(chr_num) + " >> " + out_dir + "fastq_by_Chr_" + str(chr_num) 
            print(use_cmd)
            Popen(use_cmd,shell=True).wait()
        Popen("rm -rf " + one_folder,shell=True).wait()
    print("All Done~")





if __name__ == "__main__":
    out_dir = args.out_dir
    if os.path.exists(out_dir):
        Popen("rm -rf " + out_dir,shell=True).wait()
        print("delete existing output folder: " + out_dir)
        os.makedirs(out_dir)
    else:
        os.makedirs(out_dir)
    out_dir_prefix = args.out_dir_prefix
    h5_dir = args.h5_dir
    fastq_file = args.fastq_file
    sample_name = args.sample_name
    num_of_threads = int(args.num_threads)
    chr_start = int(args.chr_start)
    chr_end = int(args.chr_end)
    #split_cmd = "zcat " + fastq_file + " | split -l 50000000 - " + out_dir + "barcoded.fastq_part"
    split_cmd = "cat " + fastq_file + " | split -l 50000000 - " + out_dir + "barcoded.fastq_part"
    Popen(split_cmd,shell=True).wait()
    Run_all_chunks(out_dir,out_dir_prefix,h5_dir,sample_name,num_of_threads,chr_start,chr_end)
    Concatenate_all(out_dir,out_dir_prefix,chr_start,chr_end)
