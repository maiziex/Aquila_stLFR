import pdb
#pdb.set_trace()
import gzip
from collections import defaultdict
import pickle
import os
from argparse import ArgumentParser


parser = ArgumentParser(description="extract qname from phased molecules:")
parser.add_argument('--fastq_file','-f',help="fastq file")
parser.add_argument('--h5_dir','-h5',help="directory for qname file")
parser.add_argument('--sample_name','-s',help="sample name")
parser.add_argument('--chr_start','-c_start',type=int,help="chromosome start from", default=1)
parser.add_argument('--chr_end','-c_end',type=int,help="chromosome end at", default=1)
parser.add_argument('--out_dir','-o_dir', help="Directory to store outputs", default='extract_fastq_files/')
args = parser.parse_args()


def get_qname_dict(chr_start,chr_end,h5_dir,sample_name):
    qname_dict = defaultdict(lambda: defaultdict(int))
    for chr_num in range(chr_start,chr_end+1):
        cur_pickle_file = h5_dir + sample_name + "_chr" + str(chr_num) + "_qname.p"
        mole_qname_dict = pickle.load(open(cur_pickle_file,"rb"))
        for mole_num, qname_list in mole_qname_dict.items():
            for qname in qname_list:
                qname_dict[qname][chr_num] = 1

    return qname_dict


def extract_fastq(barcoded_fastq_file,qname_dict,output_dir,chr_start,chr_end):
    f = open(barcoded_fastq_file,"r")
    count = 0
    flag = 0
    fw_curr = defaultdict()
    for chr_num in range(chr_start, chr_end+1):
        fw_curr[chr_num] = open(output_dir + "fastq_by_Chr_" + str(chr_num),"w")

    for line in f:
        print(count)
        data = line.rsplit()
        if count%8 == 0:
            qname_curr = data[0].split("@")[1]
            if qname_dict[qname_curr] != {}:
                flag = 1
                chr_info = qname_dict[qname_curr]
                for chr_num, _val in chr_info.items():
                    curr_chr_num = chr_num
                fw_use = fw_curr[curr_chr_num]
                fw_use.writelines(line)
                del qname_dict[qname_curr]
            else:
                del qname_dict[qname_curr]
        elif count%8 == 7:
            if flag == 1:
                fw_use.writelines(line)
                flag = 0
        else:
            if flag == 1:
                fw_use.writelines(line)

        count += 1


    print("finished.")
    f.close()
    for chr_num in range(chr_start, chr_end+1):
        fw_curr[chr_num].close()
 
    print("here")
    print(len(qname_dict))
       



if __name__ == "__main__":
    fastq_file = args.fastq_file
    h5_dir = args.h5_dir
    sample_name = args.sample_name
    output_dir = args.out_dir
    chr_start = int(args.chr_start)
    chr_end = int(args.chr_end)
    if os.path.exists(output_dir):
        print("using existing output folder: " + output_dir)
    else:
        os.makedirs(output_dir)
    for chr_num in range(chr_start,chr_end + 1):
        qname_dict = get_qname_dict(chr_num,chr_num,h5_dir,sample_name)
        extract_fastq(fastq_file,qname_dict,output_dir,chr_num,chr_num)
