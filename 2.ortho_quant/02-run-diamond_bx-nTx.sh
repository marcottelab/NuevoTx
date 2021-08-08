#!/bin/bash

NUM_THREADS=8

CUR_DIR=$(dirname $0)
MODTREE_CONF=$CUR_DIR/../"MODtree.conf"
source $MODTREE_CONF

echo "MODtree Name:" $MODTREE_NAME 
echo "MODtree Path:" $MODTREE_PATH

PARAM=" -b12 -c1 "

DB_NAME=$MODTREE_NAME
DB=$MODTREE_PATH

for FA_TX in $(ls *.fa)
do
  OUT_TX=${FA_TX/.fa/}"."$DB_NAME".dmnd_bx_tbl6"
  if [ ! -e $OUT_TX ]; then
    echo $OUT_TX
    diamond blastx $PARAM --threads $NUM_THREADS --max-target-seqs 10 --query $FA_TX --db $DB --outfmt 6 --out $OUT_TX
  fi
done
