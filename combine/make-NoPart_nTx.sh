#!/bin/bash

MKBEST="$HOME/git/NuevoTx/combine/blast_tbl-to-best_bitscore.py"
MKPART="$HOME/git/NuevoTx/combine/best-to-part.py"
MKNOPART="$HOME/git/NuevoTx/combine/make-NoPart_nTx.py"

for FA in $(ls *.combined_nTx_NR.fa)
do
  TBL=${FA/_NR.fa/_NR.self.mb+_tbl}
  BEST=${FA/_NR.fa/_NR.self.mb+_tbl_best}

  if [ ! -e $BEST ]; then
    $MKBEST $TBL
  fi

  PART=${FA/_NR.fa/_NR.self.mb+_tbl_part}
  if [ ! -e $PART ]; then
    $MKPART $BEST
  fi

  NOPART=${FA/.combined_nTx_NR.fa/}"_NoPart_nTx.fa"
  if [ ! -e $NOPART ]; then
    echo "$FA, $PART"
    $MKNOPART $FA $PART
  fi
done
