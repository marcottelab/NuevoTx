#!/bin/bash

# install kallisto first via conda
# $ conda install -c bioconda kallisto

NUM_THREADS=8
DIR_FQ="../fastq.tx/"

for FA in $(ls *.fa)
do
  IDX=${FA/.fa/}".kallisto_idx"
  echo "Make "$IDX
  kallisto index -i $IDX $FA

  OUT=${IDX/.kallisto_idx/}".kallisto_quant"

  SAMPLE_NAME=$(echo $FA | awk -F"." '{print $1}')

  # for trimmed reads
  #FQ1=$SAMPLE_NAME"_trim_1P.gz"
  #FQ1=$DIR_FQ"/"$FQ1
  #FQ2=${FQ1/_1P/_2P}

  # for raw reads
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
