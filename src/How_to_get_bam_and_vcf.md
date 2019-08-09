0. Inputs are origin paired stLFR fastq files, to preprocess it: :octocat: <br />
```
python Aquila_stLFR_fastq_preprocess.py -1 stLFR1_split_read.1.fq.gz -2 stLFR1_split_read.2.fq.gz -o S12878.fastq
```
stLFR1_split_read.1.fq.gz, stLFR1_split_read.2.fq.gz are origin stLFR paired fastq files. You can download this stLFR library from \href{ftp://ftp.cngb.org/pub/CNSA/CNP0000066/CNS0007597/CNX0005843/CNR0006054/}.


1. Inputs is 10X `fastqs` files, to get `bam` file: :octocat: <br />

To check how to download and use bwa, go to <a href="http://bio-bwa.sourceforge.net/">bwa Website</a>.
```
mkdir temp_bwa
bwa mem -t 32 -C Aquila_stLFR/source/ref.fa -p S12878.fastq  | samtools view -bS - | samtools sort -T ./temp_bwa/temp_sorting -o S12878.bam 
samtools index S12878.bam
```
S12878.fastq is the propressed stLFR fastq file. 


2. Input is `bam` file, to get `vcf` file" : :octocat: <br />
"S12878.bam" is generated from the above "bwa-mem"

```
freebayes -f Aquila_stLFR/source/ref.fa S12878.bam > S12878_freebayes.vcf 
```
