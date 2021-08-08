#!/bin/bash

DIR_IN="./msa.eggNOG50_Vertebrata"

for ALN in $(ls $DIR_IN/?/*.mafft_out.fa)
do
  OUT=${ALN/.mafft_out.fa/}".fasttree.nw"
  if [ ! -e $OUT ]; then
    echo $ALN
    fasttree $ALN > $OUT
  fi
done
