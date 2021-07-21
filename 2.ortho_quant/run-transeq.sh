#!/bin/bash

# Install EMBOSS package first using conda to run transeq.
# $ conda install -c bioconda emboss

for FA in $(ls *nTx.fa)
do
  OUT=${FA/.fa/}".transeq6.fa"
  echo $OUT
  transeq --frame 6 -sequence $FA -outseq $OUT
done
