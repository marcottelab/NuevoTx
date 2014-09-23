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
#$ -N mf.Op

FQ2MF="$HOME/git/NuevoTx/fastq/fastq-to-mult_fasta.py"
for FQ in $(ls *.fastq)
do
  $FQ2MF $FQ
done
