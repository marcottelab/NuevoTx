#!/bin/bash

VELVETG="$HOME/src.HTseq/velvet/1.2.03/velvetg-101"
VELVETH="$HOME/src.HTseq/velvet/1.2.03/velveth-101"
OASES="$HOME/src.HTseq/oases/0.2.06/oases-101"

FQ="/path/to/foobar.paired.fastq"
INS_LEN=200

for K in 55 45 35
#for K in 51 39
#for K in 47 43
do
  DIRNAME=$(basename $FQ)
  DIRNAME=${DIRNAME/.paired.fastq/}".K"$K"p"
  $VELVETH $DIRNAME $K -shortPaired -fastq $FQ
  $VELVETG $DIRNAME -read_trkg yes -ins_length $INS_LEN -cov_cutoff auto
  $OASES $DIRNAME
done 
