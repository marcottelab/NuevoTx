#!/bin/bash

#DIR_IN="MODtree.treefam"
DIR_IN="./msa.XENLA"

for ALN in $(ls $DIR_IN/*.msa_in.mafft_out)
do
  OUT=${ALN/.mafft_out/.fasttree_out}
  if [ ! -e $OUT ]; then
    echo $ALN
    fasttree $ALN > $OUT
  fi
done
