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
#$ -N p.

PAIR="$HOME/git/NuevoTx/fastq/pair-fastq.py"

for R1 in $(ls *_R1.raw.fastq*)
do
  R2=${R1/_R1/_R2}
  OUT=${R1/_R1.raw.fastq.gz/}
  OUT=${OUT/_R1.raw.fastq/}
  $PAIR $R1 $R2 $OUT
done
