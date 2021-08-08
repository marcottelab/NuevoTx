#!/bin/bash
SAMPLE=$1

for FA in $(ls *$SAMPLE*/Trinity-GG.fasta)
do
    NEW=${FA/\/Trinity-GG.fasta/.nTx.fa}
    NEW=${NEW/.trinity/}
    echo "$FA --> $NEW"
    mv $FA $NEW
done
