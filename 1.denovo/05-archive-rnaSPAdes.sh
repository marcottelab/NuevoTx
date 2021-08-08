#!/bin/bash
SAMPLE=$1

for DIR_IN in $(ls -d *$SAMPLE*.spades)
do
  echo
  TAR=$DIR_IN".tar"
  TGZ=$TAR".gz"
  echo $TAR

  if [ ! -e $TGZ ]; then
    tar cvpf $TAR --exclude="*.fastq" --exclude="*.fastg" $DIR_IN
    pigz -p 4 $TAR
  else
    echo "$TGZ exists. Skip."
  fi
done
