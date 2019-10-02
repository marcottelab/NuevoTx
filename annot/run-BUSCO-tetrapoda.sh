#!/bin/bash

FA=$1

DIR_BUSCO="$HOME/src/busco/"
DB="data/tetrapoda_odb9"

DBNAME=$(basename $DB)
OUT=$(basename $FA)
OUT=${OUT/.fa/}"."$DBNAME
python3 $DIR_BUSCO/scripts/run_BUSCO.py -i $FA -o $OUT -l $DIR_BUSCO$DB -m prot
