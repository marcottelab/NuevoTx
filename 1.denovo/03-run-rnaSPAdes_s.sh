#!/bin/bash

# Install SPAdes through bioconda
# $ conda install -c bioconda

# Ref. https://anaconda.org/bioconda/spades
# Ref. http://cab.spbu.ru/software/spades/

NUM_THREADS=8
DIR_FQ="../fastq.tx2/"

# Run trim first.
for FQ_s in $(ls $DIR_FQ/*_trim)
do
  OUT=$(basename $FQ_s)
  OUT=${OUT/_trim/}".spades"

  if [ ! -e $OUT ]; then
    echo "Make "$OUT
    rnaspades.py -s $FQ_s -t $NUM_THREADS -o $OUT
  else
    echo $OUT" exists. Skip."
  fi
done
