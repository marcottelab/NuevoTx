#!/bin/bash
for FA in $(ls *nTx.fa.gz)
do
  echo $FA
  CDNA=${FA/nTx.fa.gz/nTx.cdna.fa}
  if [ -e $CDNA ]; then
    echo "Skip "$CDNA
  else
    echo "Make "$CDNA
    ~/git/NuevoTx/annot/prot6-to-cdna+prot.py $FA
  fi
done
