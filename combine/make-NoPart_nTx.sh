#!/bin/bash

for FA in $(ls *.combined_nTx.NR_fa)
do
  PART=${FA/.NR_fa/_NR.self.mb+_tbl_part}
  echo "$FA, $PART"
  $HOME/git/NuevoTx/denovo/make-NoPart_nTx.py $FA $PART
done
