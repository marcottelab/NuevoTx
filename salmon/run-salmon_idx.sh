#!/bin/bash
NUM_THREADS=4

for FA in $(ls *_NoPart_nTx.fa)
do
  OUT=${FA/_NoPart_nTx.fa/}".salmon_idx"
  if [ ! -e $OUT ]; then
    echo "Create $OUT"
    salmon index -p $NUM_THREADS -t $FA -i $OUT
  fi
done
