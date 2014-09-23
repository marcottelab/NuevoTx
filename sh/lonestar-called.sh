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

#$ -N nc.

NOCALL="$HOME/git/NuevoTx/fastq/filter-nocall.py"
for FQ in $(ls *.fastq)
do
  echo $FQ
  $NOCALL $FQ
done
