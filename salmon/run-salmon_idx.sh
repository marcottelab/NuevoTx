#!/bin/bash
NUM_THREADS=4

# https://github.com/COMBINE-lab/salmon/releases/download/v1.0.0/salmon-1.0.0_linux_x86_64.tar.gz
SALMON_EXE="$HOME/src/salmon/salmon-1.1.0/bin/salmon"

for FA in $(ls *_NoPart_nTx.fa)
do
  OUT=${FA/_NoPart_nTx.fa/}".salmon_idx"
  if [ ! -e $OUT ]; then
    echo "Create $OUT"
    $SALMON_EXE index -p $NUM_THREADS -t $FA -i $OUT
  fi
done
