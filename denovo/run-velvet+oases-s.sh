#!/bin/bash
OASES="$HOME/git/NuevoTx/denovo/oases-101"
VELVETH="$HOME/git/NuevoTx/denovo/velveth-101"
VELVETG="$HOME/git/NuevoTx/denovo/velvetg-101"

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
