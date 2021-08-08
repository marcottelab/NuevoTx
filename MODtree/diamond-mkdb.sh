#!/bin/bash
for FA in $(ls *.fa)
do
  DB=${FA/.fa/}".dmnd"
  echo $DB
  diamond makedb --in $FA --db $DB
done
