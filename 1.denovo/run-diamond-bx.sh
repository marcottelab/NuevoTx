#!/bin/bash

NUM_THREADS=4

#DB="$HOME/pub/MODtree/2021_05/MODtree_eggNOG50_Metazoa.+GENCODE.dmnd"
#DB="$HOME/pub/MODtree/2021_05/MODtree_eggNOG50_Vertebrata.+GENCODE.2021_05.dmnd"
DB="$HOME/pub/MODtree/2021_05/MODtree_ens100.+GENCODE.2021_05.dmnd"

DB_NAME=$(basename $DB)
DB_NAME=${DB_NAME/.+GENCODE.2021_05.dmnd/}".2021_05"

for FA_TX in $(ls *gTx.fa)
do
  OUT_TX=${FA_TX/.fa/}"."$DB_NAME".dmnd_bx_tbl6"
  if [ ! -e $OUT_TX ]; then
      diamond blastx -b4 --threads $NUM_THREADS --max-target-seqs 10 --query $FA_TX --db $DB --outfmt 6 --out $OUT_TX
  fi
done
