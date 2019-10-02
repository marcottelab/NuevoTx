#!/bin/bash
for OLD in $(ls *_raw*_final.fa)
do
  NEW=${OLD/_raw/}
  NEW=${NEW/_final.fa/.fa}
  echo $OLD $NEW
  mv $OLD $NEW
done
