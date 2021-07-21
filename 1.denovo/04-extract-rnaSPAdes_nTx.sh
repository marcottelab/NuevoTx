#!/bin/bash
SAMPLE=$1

CUR_DIR=$(dirname $0)

for DIR_IN in $(ls -d *$SAMPLE*.spades)
do
  echo
  echo $DIR_IN
  $CUR_DIR/extract-rnaSPAdes_nTx.py $DIR_IN
  TGZ=$DIR_IN".tgz"
  tar cvzpf $TGZ --exclude="*.fastq" $DIR_IN
done
