#!/bin/bash

CUR_DIR=$(dirname $0)

for TX in $(ls *tx.orient.fa*)
do
  echo "Translate "$TX
  $CUR_DIR/translate-tx_orient.py $TX
done
