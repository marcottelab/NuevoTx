#!/bin/bash

curl -O http://eggnog5.embl.de/download/eggnog_5.0/e5.sequence_aliases.tsv
curl -O http://eggnog5.embl.de/download/eggnog_5.0/e5.og_annotations.tsv
curl -O http://eggnog5.embl.de/download/eggnog_5.0/e5.taxid_info.tsv

# 33208_Metazoa

TAX_ID=33208
URL="http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level"

for FILE in _members.tsv.gz _annotations.tsv.gz _raw_algs.tar _trimmed_algs.tar _trees.tsv.gz _hmms.tar
do
  echo $URL/$TAX_ID/$TAX_ID$FILE
  curl -O $URL/$TAX_ID/$TAX_ID$FILE
done

#33208/33208_members.tsv.gz
#http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/33208/33208_annotations.tsv.gz
#http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/33208/33208_trimmed_algs.tar
#http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/33208/33208_trees.tsv.gz
#http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/33208/33208_raw_algs.tar
