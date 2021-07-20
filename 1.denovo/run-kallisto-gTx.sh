#!/bin/bash

NUM_THREADS=8
DIR_FQ="../fastq.JBL055/"

for FA in $(ls *.gTx.fa)
do
  IDX=${FA/.fa/}".kallisto_idx"
  echo "Make "$IDX
  kallisto index -i $IDX $FA

  OUT=${IDX/.kallisto_idx/}".kallisto_quant"

  SAMPLE_NAME=$(echo $FA | awk -F"." '{print $1}')
  FQ1=$SAMPLE_NAME"_R1.raw.fastq.gz"
  FQ1=$DIR_FQ"/"$FQ1
  FQ2=${FQ1/_R1/_R2}
  echo "FASTQ:" $FQ1 $FQ2

  if [ -d $OUT ]; then
    echo "$OUT exists. Skip."
  else
    echo "Run $OUT"
    kallisto quant -t $NUM_THREADS -i $IDX -o $OUT $FQ1 $FQ2
  fi
done
