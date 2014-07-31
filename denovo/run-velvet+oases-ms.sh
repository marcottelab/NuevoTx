#!/bin/bash

OASES="$HOME/git/NuevoTx/denovo/oases-101"
VELVETH="$HOME/git/NuevoTx/denovo/velveth-101"
VELVETG="$HOME/git/NuevoTx/denovo/velvetg-101"

FA_m="/path/to/foobar.mult_fasta"
FA_s=${FA_m/mult_fasta/single_fasta}

for K in 55 45 35
#for K in 51 39
#for K in 47 43
do
  DIRNAME=$(basename $FA_m)
  DIRNAME=${DIRNAME/.mult_fasta/}".K"$K"ms"
  $VELVETH $DIRNAME $K -short -fasta $FA_m -short -fasta $FA_s
  $VELVETG $DIRNAME -read_trkg yes -cov_cutoff auto
  $OASES $DIRNAME
done
