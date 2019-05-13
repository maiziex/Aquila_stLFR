1. Inputs is 10X `fastqs` files, to get `bam` file: :octocat: <br />

To check how to download and use bwa, go to <a href="http://bio-bwa.sourceforge.net/">bwa Website</a>.
```
mkdir temp_bwa
bwa mem -t 32 -C Aquila_stLFR/source/ref.fa -p S12878.fastq  | samtools view -bS - | samtools sort -T ./temp_bwa/temp_sorting -o S12878.bam 
samtools index S12878.bam
```



2. Input is `bam` file, to get `vcf` file" : :octocat: <br />
"S12878.bam" is generated from the above "bwa-mem"

```
freebayes -f Aquila_stLFR/source/ref.fa S12878.bam > S12878_freebayes.vcf 
```
