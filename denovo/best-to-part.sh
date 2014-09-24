#!/bin/bash

for BEST in $(ls *best)
do
  echo $BEST
  $HOME/git/NuevoTx/denovo/best-to-part.py $BEST
done
