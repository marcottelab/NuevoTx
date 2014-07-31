#!/bin/bash
#SBATCH -o os.o%j
#SBATCH -J "os.foo"

#$ -N os.foo

VELVETG="$HOME/src.HTseq/velvet/1.2.03/velvetg-101"
VELVETH="$HOME/src.HTseq/velvet/1.2.03/velveth-101"
OASES="$HOME/src.HTseq/oases/0.2.06/oases-101"

FQ="/path/to/foobar.called.fastq"

for K in 55 45 35
#for K in 51 39
#for K in 47 43
do
  DIRNAME=$(basename $FQ)
  DIRNAME=${DIRNAME/.called.fastq/}".K"$K"s"
  $VELVETH $DIRNAME $K -short -fastq $FQ 
  $VELVETG $DIRNAME -read_trkg yes -cov_cutoff auto
  $OASES $DIRNAME
done
