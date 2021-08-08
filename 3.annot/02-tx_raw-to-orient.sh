#!/bin/bash

CUR_DIR=$(dirname $0)

for TX in $(ls *tx.raw.fa*)
do
  $CUR_DIR/tx_raw-to-tx_orient.py $TX
done
