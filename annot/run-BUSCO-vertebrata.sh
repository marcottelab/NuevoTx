#!/bin/bash

#python3 ./scripts/run_BUSCO.py -i AmphiBase/Hynobius_retardatus.AB2019_05.prot.fa -o Hynobius_retardatus.busco -l data/vertebrata_odb9/ -m prot

FA=$1

DIR_BUSCO="$HOME/src/busco/"
DB="data/vertebrata_odb9"

FA=$1

DBNAME=$(basename $DB)
OUT=$(basename $FA)
OUT=${OUT/.fa/}"."$DBNAME
python3 $DIR_BUSCO/scripts/run_BUSCO.py -i $FA -o $OUT -l $DIR_BUSCO$DB -m prot
