#!/usr/bin/env python
import gzip
from argparse import ArgumentParser
import sys
parser = ArgumentParser(description="Preprocessing paired fastq files for Aquila_stLFR\n",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--fastq_1','-1',help="origin stLFR fastq 1 (gz file)",required=True)
parser.add_argument('--fastq_2','-2',help="origin stLFR fastq 2 (gz file)",required=True)
parser.add_argument('--out_file','-o',help="output stLFR fastq file for Aquila_stLFR",default="stLFR_fastq_for_Aquila.fastq")
args = parser.parse_args()


def merge_paired_reads(read1_file,read2_file,out_file):
    fw = open(out_file,"w")
    count = 0
    with gzip.open(read1_file,"r") as f1, gzip.open(read2_file,"r") as f2:
        for line1,line2 in zip(f1,f2):
            if count%4 == 0:
                data1 = line1.decode().rsplit()
                data2 = line2.decode().rsplit()
                qname1 = data1[0].split("#")[0]
                barcode1 = data1[0].split("#")[1].split("/")[0]
                qname2 = data2[0].split("#")[0]
                barcode2 = data2[0].split("#")[1].split("/")[0]
                fw.writelines(qname1 + "\t" + "BX:Z:" + barcode1 + "\n")
                line5 = qname2 + "\t" + "BX:Z:" + barcode2 + "\n"
            elif count%4 == 1:
                fw.writelines(line1.decode())
                line6 = line2.decode() 
            elif count%4 == 2:
                fw.writelines(line1.decode())
                line7 = line2.decode() 
            elif count%4 == 3:
                fw.writelines(line1.decode())
                line8 = line2.decode() 
                fw.writelines(line5)
                fw.writelines(line6)
                fw.writelines(line7)
                fw.writelines(line8)
            count += 1                
    fw.close()


def main():
    if len(sys.argv) == 1:
        Popen("python3 " + "Aquila_stLFR_fastq_preprocess.py -h",shell=True).wait()
    else:
        fastq_1 = args.fastq_1    
        fastq_2 = args.fastq_2    
        out_file = args.out_file  
        merge_paired_reads(fastq_1,fastq_2,out_file)


if __name__ == "__main__":
    main()

