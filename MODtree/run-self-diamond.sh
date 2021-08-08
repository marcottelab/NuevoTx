#!/bin/bash

FA=$1

DB=${FA/.fa/}".dmnd"

DBNAME=$(basename $DB)
DBNAME=$(echo $DBNAME | awk -F"." '{print $1}')

NUM_THREADS=4

if [ ! -e $DB ]; then
  echo "Make DIAMOND DB ($DBNAME): $DB"
  diamond makedb --in $FA --db $DB
else
  echo "$DB exists. Skip makedb."
fi

OUT=${FA/.fa/}".self.dmnd_bp_out6"
echo $OUT
diamond blastp --threads $NUM_THREADS --db $DB --query $FA --outfmt 6 --out $OUT 
