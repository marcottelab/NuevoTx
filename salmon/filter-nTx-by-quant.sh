#!/bin/bash

for NTX in $(ls *_NoPart_nTx.fa)
do
  OUT=${NTX/_NoPart_nTx.fa/}"_NoPartQuant_nTx.fa"
  if [ -e $OUT ]; then
    echo $OUT" exists. Skip."
  else
    echo "Make "$OUT
    $(dirname $0)/filter-nTx-by-quant.py $NTX > $OUT
  fi
done
