#!/bin/bash
SAMPLE=$1

for FA in $(ls *$SAMPLE*/transcripts.fa)
do
    NEW=${FA/\/transcripts.fa/.nTx.fa}
    echo "$FA --> $NEW"
    mv $FA $NEW
done

for FA in $(ls *$SAMPLE*/contigs.fa)
do
    NEW=${FA/\/contigs.fa/.nTx_ctg.fa}
    echo "$FA --> $NEW"
    mv $FA $NEW
done
