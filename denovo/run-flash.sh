#!/bin/bash

NUM_THREADS=4
MAX_OVERLAP=90

for R1 in $(ls *_trim_1P)
do
  R2=${R1/_1P/_2P}
  #OUT_NAME=$(echo $R1 | awk -F ".R1" '{print $1}')
  OUT_NAME=${R1/_trim_1P/}
  echo $R1 $R2 $OUT_NAME
  flash $R1 $R2 -o $OUT_NAME -t $NUM_THREADS -M $MAX_OVERLAP --interleaved-output
done


