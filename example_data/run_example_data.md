#### We provide a small chromosome's (**chr21**) example dataset to run the whole pipeline before you try it to the large dataset. 

Please download the example data <a href="https://zenodo.org/record/5032380">from Zenodo</a>.
```
Aquila_stLFR_exampledata
|-test.fastq
|
|-test.bam (hg19)
|-test.bam.bai
|
|-test_freebayes.vcf (hg19)
|
|-genome_hg19.fa         
```

Please download hg19 "Uniqness_map" folder by wget 
```
wget http://xinzhouneuroscience.org/wp-content/uploads/2019/06/Uniqness_map_hg19.tar.gz 
```

Run the whole pipeline:
```
python Aquila_stLFR/bin/Aquila_stLFR_step1.py --bam_file test.bam --vcf_file test_freebayes.vcf --sample_name test --chr_start 21 --chr_end 21 --out_dir test_asm --uniq_map_dir Uniqness_map_hg19 --fastq_file test.fastq

python Aquila_stLFR/bin/Aquila_stLFR_step2.py --chr_start 21 --chr_end 21 --out_dir test_asm --num_threads 30 --num_threads_spades 20 --reference genome_hg19.fa

python Aquila_stLFR/bin/Aquila_stLFR_assembly_based_variants_call.py  --assembly_dir test_asm  --ref_file genome_hg19.fa  --num_of_threads 2 --out_dir test_variant_results --var_size 1 --chr_start 21 --chr_end 21 --all_regions_flag 1

python Aquila_stLFR/bin/Aquila_stLFR_phasing_all_variants.py --assembly_vcf test_variant_results/Aquila_final_sorted.vcf --vcf_file test_freebayes.vcf --assembly_dir test_asm --chr_start 21 --chr_end 21

```
