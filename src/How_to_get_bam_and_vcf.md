1. Inputs is 10X `fastqs` files, to get `bam` file: :octocat: <br />

To check how to download and use "longranger align" or download human reference genome, go to <a href="https://support.10xgenomics.com/genome-exome/software/downloads/latest">10X GENOMICS Website</a>.
```
mkdir temp_bwa
bwa mem -t 32 -C -R '@RG\tID:7597:LibraryNotSpecified:1:unknown_fc:0\tSM:7597' Aquila_stLFR/source/ref.fa -p S12878.fastq  | samtools view -bS - | samtools sort -T ./temp_bwa/temp_sorting -o S12878.bam 
samtools index S12878.bam
```



2. Input is `bam` file, to get `vcf` file" : :octocat: <br />
"possorted_bam.bam" is generated from the above "longranger align"

```
freebayes -f Aquila_stLFR/source/ref.fa S12878.bam > S12878_freebayes.vcf 
```
