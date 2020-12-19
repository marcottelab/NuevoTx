#!/bin/bash

DB="$HOME/pub/MODtree/2020_05/MODtree_ENOG50.uniprot+gencode.dmnd"
DBNAME=$(basename $DB)
DBNAME=${DBNAME/.uniprot+gencode.dmnd/}

NUM_THREADS=8

for FA in $(ls *.prot6.fa)
do
  OUT=${FA/.fa/}"."$DBNAME".dmnd_bp_out"
  echo $OUT
  diamond blastp --threads $NUM_THREADS --db $DB --query $FA --outfmt 6 --out $OUT 
done
