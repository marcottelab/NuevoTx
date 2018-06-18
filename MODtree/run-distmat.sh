#!/bin/bash

#DIR_IN="MODtree.treefam"
DIR_IN="./msa.XENLA"

for ALN in $(ls $DIR_IN/*.msa_in.mafft_out)
do
  OUT=${ALN/.mafft_out/.distmat_out}
  if [ ! -e $OUT ]; then
    echo $ALN
    distmat -protmethod 1 -sequence $ALN -outfile $OUT
  fi
done
