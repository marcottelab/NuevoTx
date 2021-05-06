#!/bin/bash

NUM_THREADS=4

#DB="$HOME/pub/MODtree/2021_05/MODtree_eggNOG50_Metazoa.+GENCODE.dmnd"
#DB="$HOME/pub/MODtree/2021_05/MODtree_eggNOG50_Vertebrata.+GENCODE.dmnd"
#DB="$HOME/pub/MODtree/2021_05/MODtree_ens100.+GENCODE.dmnd"

for DB in $(ls $HOME/pub/MODtree/2021_05/*.+GENCODE.2021_05.dmnd)
do
  DB_NAME=$(basename $DB)
  DB_NAME=${DB_NAME/.+GENCODE.2021_05.dmnd/}

  FA_TX="XENTR_XB201901_pep.fa"

  #for FA_TX in $(ls *nTx_NR.fa)
  #for FA_TX in $(ls *nTx.fa)
  #do
    OUT_TX=${FA_TX/.fa/}"."$DB_NAME".dmnd_bx_tbl6"
    if [ ! -e $OUT_TX ]; then
      diamond blastp --threads $NUM_THREADS --max-target-seqs 10 --query $FA_TX --db $DB --outfmt 6 --out $OUT_TX
    fi
  #done
done
