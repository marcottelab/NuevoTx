#!/bin/bash

NUM_THREADS=4
MAX_OVERLAP=140

for R1 in $(ls *_1P)
do
  R2=${R1/_1P/_2P}
  #OUT_NAME=$(echo $R1 | awk -F ".R1" '{print $1}')
  OUT_NAME=${R1/_trimmed_1P/}
  echo $R1 $R2 $OUT_NAME
  flash $R1 $R2 -o $OUT_NAME -t $NUM_THREADS -M 140 --interleaved-output
done

