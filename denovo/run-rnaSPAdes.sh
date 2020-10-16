#!/bin/bash


# Install SPAdes through bioconda
# $ conda install -c bioconda

# Ref. https://anaconda.org/bioconda/spades
# Ref. http://cab.spbu.ru/software/spades/

NUM_THREADS=8
DIR_FQ="../fastq.TKLab202010/"

# Run trim+flash first.
for FQ_e in $(ls $DIR_FQ/*Testis*.extendedFrags.fastq)
do
  FQ_nc=${FQ_e/.extendedFrags.fastq/}".notCombined.fastq"
  OUT=$(basename $FQ_e)
  OUT=${OUT/.extendedFrags.fastq/}".spades"
  if [ ! -e $OUT ]; then
    echo "Make "$OUT
    rnaspades.py --merged $FQ_e --12 $FQ_nc -t $NUM_THREADS -o $OUT
  else
    echo $OUT" exists. Skip."
  fi
done
