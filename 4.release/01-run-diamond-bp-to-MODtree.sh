#!/bin/bash

NUM_THREADS=4

CUR_DIR=$(dirname $0)
MODTREE_CONF=$CUR_DIR/../"MODtree.conf"
source $MODTREE_CONF

echo "MODtree Name:" $MODTREE_NAME 
echo "MODtree Path:" $MODTREE_PATH

DB=$MODTREE_PATH
DB_NAME=$MODTREE_NAME

FA=$1

OUT_TBL=${FA/.fa/}"."$DB_NAME".dmnd_bp_tbl6"
if [ ! -e $OUT_TBL ]; then
      diamond blastp -b4 --threads $NUM_THREADS --max-target-seqs 10 --query $FA --db $DB --outfmt 6 --out $OUT_TBL
fi
