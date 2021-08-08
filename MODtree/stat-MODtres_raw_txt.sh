#!/bin/bash

for RAW_TXT in $(ls MODtree*.raw.txt)
do
  SPECIES=${RAW_TXT/.raw.txt/}".species_freq.txt"
  FAMILY=${RAW_TXT/.raw.txt/}".family_freq.txt"
  if [ ! -e $SPECIES ]; then
    awk '{print $4}' $RAW_TXT | sort | uniq -c | sort -nr > $SPECIES
  fi

  if [ ! -e $FAMILY ]; then
    awk '{print $2}' $RAW_TXT | sort | uniq -c | sort -nr > $FAMILY
  fi
done
