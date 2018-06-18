#!/bin/bash
NUM_THREADS=1

#DIR_IN="MODtree.treefam"
DIR_IN="./msa.XENLA"

for IN in $(ls $DIR_IN/*[01234].msa_in.fa)
do
  OUT=${IN/.fa/.mafft_out}

  if [ ! -e $OUT ]; then
    echo "$IN -> $OUT"
    mafft --anysymbol --maxiterate 1000 --reorder --thread $NUM_THREADS --quiet --localpair $IN > $OUT
  else
    echo "Skip $OUT"
  fi
done
