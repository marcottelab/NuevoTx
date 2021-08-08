#!/bin/bash

URL_BASE="http://eggnog5.embl.de/download/eggnog_5.0"
for FILE in e5.sequence_aliases.tsv e5.og_annotations.tsv e5.taxid_info.tsv e5.level_info.tar.gz
do
  echo $URL_BASE/$FILE
  curl -O $URL_BASE/$FILE
done

URL_TAX="http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level"

# For all files
# for FILE in _members.tsv.gz _annotations.tsv.gz _raw_algs.tar _trimmed_algs.tar _trees.tsv.gz _hmms.tar

# For files only required for MODtree
for FILE in _members.tsv.gz _annotations.tsv.gz _raw_algs.tar
do
  # Taxonomy ID
  # 7742=Vertebrata, 33208=Metazoa
  for TAX_ID in 7742 33208
  do
    echo $URL_TAX/$TAX_ID/$TAX_ID$FILE
    curl -O $URL_TAX/$TAX_ID/$TAX_ID$FILE
  done
done

#33208/33208_members.tsv.gz
#http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/33208/33208_annotations.tsv.gz
#http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/33208/33208_trimmed_algs.tar
#http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/33208/33208_trees.tsv.gz
#http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/33208/33208_raw_algs.tar
