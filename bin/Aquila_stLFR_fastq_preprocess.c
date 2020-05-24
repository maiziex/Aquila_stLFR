/*********************************************************************/
/* PROGRAM	Aquila_stLFR_fastq_preprocess.c			*/
/* DATE	23-MAY-2020						*/
/*									*/
/* DESCRIPTION	Reads two compressed (gz) fastq files 		*/
/*		Combines and saves into third merged file		*/
/*									*/
/* USAGE	./Aquila_stLFR_fastq_preprocess			*/ 
/*		-1 stLFR1_split_read.1.fq.gz				*/ 
/*		-2 stLFR1_split_read.2.fq.gz 				*/
/*		-o S12878.fastq					*/
/* 									*/
/* NOTES 	installing zlib is necessary for reading .gz files	*/
/*		Uses Heng Li's C readfq function 			*/
/*		https://github.com/lh3/readfq				*/
/*********************************************************************/


#include <zlib.h>

#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <math.h>
#include "kseq.h"


#define MAXCHAR	1000

/* Function prototypes */
void 	readseq();

KSEQ_INIT(gzFile, gzread)

static int usage()
{	printf("Program: Aquila_stLFR_fastq_preprocess\n");
        printf("Usage: Aquila_stLFR_fastq_preprocess -1 <read1_input_fq.gz> -2 <read2_input_fq.qz> -o <output_merged.fq> \n");
        printf("\n");
        return 1;
}

/* Global variables */
FILE	*outfile;
char	infilename1[MAXCHAR], infilename2[MAXCHAR], outfilename[MAXCHAR];
kseq_t *seq1, *seq2;



/**********************************************************************
/* main()								*/
/*									*/
/* Opens input and output files and calls readseq to construct file	*/
/* process input and write to output					*/
/**********************************************************************/
int main(int argc, char *argv[])
{ gzFile fp1, fp2;
  
  /* all 3 filenames entered in command line */
  if( (argc!=7) || strcmp(argv[1],"-1") || strcmp(argv[3],"-2") || strcmp(argv[5],"-o") )
  return usage();
  else
    { strcpy(infilename1,argv[2]);
      strcpy(infilename2,argv[4]);
      strcpy(outfilename,argv[6]);
    }
    
    /* open input and output files */
    fp1 = gzopen(infilename1, "r");
    if (! fp1)
        {   printf ("gzopen of '%s' failed\n", infilename1);
            return 1;
        }
    seq1 = kseq_init(fp1);

    fp2 = gzopen(infilename2, "r");
    if (! fp2)
        {   printf ("gzopen of '%s' failed\n", infilename2);
            return 1;
        }
    seq2 = kseq_init(fp2);
    
    outfile = fopen(outfilename, "wt");

    /* process the read sequences here */
    readseq();


    /* Close files */ 
    kseq_destroy(seq1);
    kseq_destroy(seq2);
    gzclose(fp1);
    gzclose(fp2);
    fclose(outfile);

    return 0;
}   



/**********************************************************************
/* readseq()								*/
/*									*/
/* This is the main body of the program 				*/
/* It retrieves each read constructs the merged line and saves ouput */	
/*********************************************************************/
void readseq()
{ int i, readlength, n=0;
  char readname[MAXCHAR];

    
  /* read fastq files */
    
  while (kseq_read(seq1) >= 0)
  {   n++;
      kseq_read(seq2);
    
      readlength=strlen(seq1->name.s);

      /* Create first merged read of pair */
      readname[0]='@';
      for (i=0; i<readlength; i++)
      { if (seq1->name.s[i]=='#')
        { readname[i+1]=0;
          break;
        }
      else
        readname[i+1]=seq1->name.s[i];
      }
    
      strcat(readname,"\tBX:Z:");
      for (i=i+1; i<strlen(seq1->name.s); i++)
      { if (seq1->name.s[i]=='/')
        { readname[i+6]=0;
          break;
        }
      else
        readname[i+6]=seq1->name.s[i];
      }
      fprintf(outfile, "%s\n%s\n+\n%s\n",readname,seq1->seq.s,seq1->qual.s);


      /* repeat for second read - name should be identical but copy regardless */
      for (i=0; i<readlength; i++)
      { if (seq2->name.s[i]=='#')
          break;
      else
        readname[i+1]=seq2->name.s[i];
      }
      for (i=i+1; i<strlen(seq1->name.s); i++)
      { if (seq2->name.s[i]=='/')
          break;
      else
        readname[i+6]=seq2->name.s[i];
      }
      fprintf(outfile, "%s\n%s\n+\n%s\n",readname,seq2->seq.s,seq2->qual.s);
    }

    printf("Processed number of read pairs: %d\n", n);   
} 




