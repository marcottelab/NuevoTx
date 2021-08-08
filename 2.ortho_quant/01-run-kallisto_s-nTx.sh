#!/bin/bash

# install kallisto first via conda
# $ conda install -c bioconda kallisto

NUM_THREADS=8
DIR_FQ="../fastq.tx2/"

for FA in $(ls *.fa)
do
  IDX=${FA/.fa/}".kallisto_idx"
  echo "Make "$IDX
  kallisto index -i $IDX $FA

  OUT=${IDX/.kallisto_idx/}".kallisto_quant"

  SAMPLE_NAME=$(echo $FA | awk -F"." '{print $1}')

  # for trimmed reads
  FQ1=$SAMPLE_NAME"_trim.fq"
  FQ1=$DIR_FQ"/"$FQ1

  # for raw reads
  #FQ1=$SAMPLE_NAME"_trim.fq"
  #FQ1=$DIR_FQ"/"$FQ1

  echo "FASTQ:" $FQ1 

  if [ -d $OUT ]; then
    echo "$OUT exists. Skip."
  else
    echo "Run $OUT"
    FRAGMENT_LEN=200
    FRAGMENT_LEN_SD=0.1

    kallisto quant --single -l $FRAGMENT_LEN -s $FRAGMENT_LEN_SD \
                   -t $NUM_THREADS -i $IDX -o $OUT $FQ1
  fi
done
