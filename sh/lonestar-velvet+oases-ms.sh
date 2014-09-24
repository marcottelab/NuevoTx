#!/bin/bash
#$ -V                   # Inherit the submission environment
#$ -cwd                 # Start job in submission directory
#$ -j y                 # Combine stderr and stdout
#$ -o $JOB_NAME.o$JOB_ID
#$ -pe 1way 12          # Change it to '1way 25' for 'largemem' queue
#$ -q normal            # Change it to 'largemem' if you need more memory
#$ -l h_rt=24:00:00     # Run time (hh:mm:ss)
#$ -M $EMAIL
#$ -m be                # Email at Begin and End of job
#$ -P hpc

set -x 

OASES="$HOME/git/NuevoTx/denovo/oases-101"
VELVETH="$HOME/git/NuevoTx/denovo/velveth-101"
VELVETG="$HOME/git/NuevoTx/denovo/velvetg-101"

#$ -N oms.foobar.543

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
