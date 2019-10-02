#!/bin/bash
# OUT_NAME="Hynobius_quelpaertensis.AB2019_05"
OUT_NAME=$1

for SUFFIX in cdna.fa prot.fa ncdna.fa orphan_cdna.fa orphan_prot.fa id_list prot_targets
do
  echo $SUFFIX
  cat ../prot6/*.$SUFFIX > $OUT_NAME"_raw."$SUFFIX
done

#~/git/NuevoTx/annot/prot_targets-to-names.py $OUT_NAME"_raw.prot_targets"
#~/git/NuevoTx/annot/make-final.py $OUT_NAME"_raw.prot_names"

#mkdir $OUT_NAME"_raw"
#mv $OUT_NAME* $OUT_NAME"_raw"
