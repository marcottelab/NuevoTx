#!/bin/bash

URL="ftp://ftp.uniprot.org/pub/databases/uniprot/current_release"
echo "Download ReleaseNotes ..."
curl -O $URL"/relnotes.txt"
echo "Download SpeciesList ..."
curl -O https://www.uniprot.org/docs/speclist

SRC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REF_LIST=$SRC_DIR"/MODtree_species.txt"

if [ ! -e $REF_LIST ]; then
  echo "Not available: Uniprot Ref Proteome List"
  echo "Current setting: "$REF_LIST
  exit
fi

for UP_ID in $(grep -v ^# $REF_LIST | awk '{print $1"_"$2}')
do
  echo $UP_ID
  #for SUFFIX in ".fasta.gz" "_DNA.fasta.gz" ".gene2acc.gz" ".idmapping.gz"
  for SUFFIX in ".fasta.gz"
  do
    TARGET_FILE=$UP_ID$SUFFIX
    if [ ! -e $TARGET_FILE ]; then
      echo "Download "$TARGET_FILE
      curl -O ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Eukaryota/$TARGET_FILE
    else
      echo $TARGET_FILE" exists. Skip."
    fi
  done
done
