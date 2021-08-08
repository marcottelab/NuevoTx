#!/bin/bash

#DIR_IN="./msa.ens100"
#DIR_IN="./msa.eggNOG50_Vertebrata"
DIR_IN="./msa.eggNOG50_Metazoa"

for ALN in $(ls $DIR_IN/?/*.mafft_out.fa)
do
  OUT=${ALN/.mafft_out.fa/}".distmat"
  if [ ! -e $OUT ]; then
    echo $ALN
    distmat -protmethod 1 -sequence $ALN -outfile $OUT
  fi
done
