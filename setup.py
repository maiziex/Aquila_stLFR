from setuptools import setup, find_packages, Extension

setup(name='aquila_stlfr',
      version='1.1',
      description='assembly and variant calling for stlfr and hybrid assembler for linked-reads',
      author='XinZhou',
      author_email='xzhou15@cs.stanford.edu',
      packages=['bin',],
      entry_points={'console_scripts':['Aquila_stLFR_step1=bin.Aquila_stLFR_step1:main','Aquila_step1_hybrid=bin.Aquila_step1_hybrid:main','Aquila_stLFR_step2=bin.Aquila_stLFR_step2:main','Aquila_stLFR_assembly_based_variants_call=bin.Aquila_stLFR_assembly_based_variants_call:main','Aquila_stLFR_phasing_all_variants=bin.Aquila_stLFR_phasing_all_variants:main','Aquila_stLFR_clean=bin.Aquila_stLFR_clean:main','Aquila_step0_sortbam_hybrid=bin.Aquila_step0_sortbam_hybrid:main','Aquila_stLFR_fastq_preprocess=bin.Aquila_stLFR_fastq_preprocess:main']},
      zip_safe=False)
