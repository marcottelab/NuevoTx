#!/bin/bash

NUM_THREADS=4
DIR_FQ="../fastq.TKLab201907n"

for FA in $(ls *_NoPart_nTx.fa)
do
  IDX=${FA/_NoPart_nTx.fa/.salmon_idx}
  OUT=${FA/_NoPart_nTx.fa/.salmon_quant}
  FQ1=${FA/_NoPart_nTx.fa/}"_R1.raw.fastq.gz"
  FQ1=$DIR_FQ"/"$FQ1
  FQ2=${FQ1/_R1/_R2}

  if [ ! -d $IDX ]; then
    echo "Run run-salmon_idx.sh first."
    exit
  elif [ -d $OUT ]; then
    echo "$OUT exists. Skip."
  else
    echo "Run $OUT"
    salmon quant -p $NUM_THREADS -i $IDX -l A --validateMappings -1 $FQ1 -2 $FQ2 -o $OUT
  fi
done

