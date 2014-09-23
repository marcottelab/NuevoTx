#!/bin/bash
#$ -V
#$ -cwd
#$ -j y
#$ -o $JOB_NAME.o$JOB_ID
#$ -pe 1way 12
#$ -q normal
#$ -l h_rt=24:00:00
#$ -M $EMAIL
#$ -m be
#$ -P hpc

set -x
#$ -N p6. 
TN="$HOME/git/NuevoTx/fasta/translate-tx2prot6"

for FA in $(ls *.fa)
do
  $TN $FA 
done
