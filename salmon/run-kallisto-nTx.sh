#!/bin/bash

NUM_THREADS=8
DIR_FQ="../fastq/"

for FA in $(ls *_nTx_NR.fa)
do
  IDX=${FA/.fa/}".kallisto_idx"
  echo "Make "$IDX
  kallisto index -i $IDX $FA

  OUT=${IDX/.kallisto_idx/}".kallisto_quant"

  SAMPLE_NAME=$(echo $FA | awk -F"." '{print $1}')
  FQ1=$SAMPLE_NAME"_trim_1P.gz"
  FQ1=$DIR_FQ"/"$FQ1
  FQ2=${FQ1/_1P/_2P}
  echo "FASTQ:" $FQ1 $FQ2

  if [ -d $OUT ]; then
    echo "$OUT exists. Skip."
  else
    echo "Run $OUT"
    kallisto quant -t $NUM_THREADS -i $IDX -o $OUT $FQ1 $FQ2
  fi
done
