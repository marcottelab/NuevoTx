#!/bin/bash
TBL_CODON="tbl01.standard"

if [$1 != '']; then
  TBL_CODON=$1
fi

for FA in $(ls *nTx.fa)
do
  $HOME/git/NuevoTx/prot6/translate-tx2prot6.py $FA $TBL_CODON
done
