#!/bin/bash

for BEST in $(ls *best)
do
  echo $BEST
  $HOME/git/NuevoTx/combine/best-to-part.py $BEST
done
