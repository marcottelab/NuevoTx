#!/bin/bash

BEST=$(dirname $0)"/best_tbl-to-best_bitscore.py"

for TBL in $(ls | egrep '_tbl(.gz)*$')
do
  OUT=$TBL"_best"
  if [ ! -e $OUT ]; then
    echo $TBL
    $BEST $TBL
  fi
done
