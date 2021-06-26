#!/bin/bash

## Assume that you install trimmomatic with conda
## Directory for conda

DIR_CONDA=$HOME/miniconda3
NUM_THREADS=4
ADAPTER_TYPE="TruSeq2-PE.fa"

FA_ADAPTER=$( find $DIR_CONDA | grep -m1 $ADAPTER_TYPE )
echo "Adapter: "$FA_ADAPTER
cp $FA_ADAPTER .

#pigz -p 4 -d *fastq.gz

for FQ1 in $(ls *R1.raw.fastq.gz)
do
  FQ2=${FQ1/_R1/_R2}
  OUT=${FQ1/_R1.raw.fastq.gz}"_trim"
  echo $FQ1 $FQ2 $OUT

  trimmomatic PE -threads $NUM_THREADS -validatePairs \
   -summary $OUT".summary" $FQ1 $FQ2 -baseout $OUT \
   ILLUMINACLIP:$ADAPTER_TYPE:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:50
done

