You can download the example data <a href="https://drive.google.com/drive/folders/1h6Ln1opf5vTAMjuUzmDzb9RgV7n1ybZi?usp=sharing">here</a>.
```
Aquila_stLFR_exampledata
|-test.fastq
|
|-test.bam 
|
|-test_freebayes.vcf 
|
|-refdata-hg19-2.1.0
|   └fasta 
|       └genome.fa
```

To run the whole pipeline:
```
python Aquila_stLFR/bin/Aquila_stLFR_step1.py --bam_file test.bam --vcf_file test_freebayes.vcf --sample_name test --chr_start 21 --chr_end 21 --out_dir test_asm --uniq_map_dir Uniqness_map_hg19/ --fastq_file test.fastq

python Aquila_stLFR/bin/Aquila_stLFR_step2.py --chr_start 21 --chr_end 21 --out_dir test_asm --num_threads 40 --num_threads_spades 20 --reference /oak/stanford/groups/arend/Xin/Software/refdata-hg19-2.1.0/fasta/genome.fa

python Aquila_stLFR/bin/Aquila_stLFR_assembly_based_variants_call.py  --assembly_dir test_asm  --ref_file refdata-hg19-2.1.0//fasta/genome.fa  --num_of_threads 2 --out_dir test_variant_results --var_size 1 --chr_start 21 --chr_end 21 --all_regions_flag 1

python Aquila_stLFR/bin/Aquila_stLFR_phasing_all_variants.py --assembly_vcf test_variant_results/Aquila_final_sorted.vcf --vcf_file test_freebayes.vcf --assembly_dir test_asm --chr_start 21 --chr_end 21

```
