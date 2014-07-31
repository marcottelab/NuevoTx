#!/bin/bash
SAMPLE=$1
for FA in $(ls *$SAMPLE*/transcripts.fa)
do
    NEW=${FA/\/transcripts.fa/.nTx.fa}
    echo "$FA --> $NEW"
    mv $FA $NEW
done
