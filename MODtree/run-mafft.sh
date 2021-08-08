#!/bin/bash
NUM_THREADS=4

#DIR_IN="./msa.eggNOG50_Vertebrata"
DIR_IN="./msa.eggNOG50_Metazoa"

for IN in $(ls $DIR_IN/?/*.msa_in.fa)
do
  OUT=${IN/.msa_in.fa/.mafft_out.fa}

  if [ ! -e $OUT ]; then
    echo "$IN -> $OUT"
    mafft --anysymbol --maxiterate 1000 --reorder --thread $NUM_THREADS \
          --quiet --localpair $IN > $OUT
  else
    echo "Skip $OUT"
  fi
done
