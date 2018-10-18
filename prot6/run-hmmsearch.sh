#!/bin/bash

HMM_LIB="$HOME/pub/Pfam/Pfam32.0/Pfam-A.hmm"
NUM_THREADS=3

TBL=${FA/.fa/}".hmmer_tbl"

for FA in $(ls *prot6.fa)
do
  hmmsearch --tblout $TBL --cpu $NUM_THREADS $HMM_LIB $FA > /dev/null
done
