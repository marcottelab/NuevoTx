#!/bin/bash

curl -O ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/relnotes.txt
curl -O https://www.uniprot.org/docs/speclist

SRC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REF_LIST=$SRC_DIR"/MODtree_species.txt"

if [ ! -e $REF_LIST ]; then
  echo "Not available: Uniprot Ref Proteome List"
  echo "Current setting: "$REF_LIST

else

  for UP_ID in $(grep -v ^# $REF_LIST | awk '{print $1"_"$2}')
  do
    echo $UP_ID
    curl -O ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Eukaryota/$UP_ID".fasta.gz"
    curl -O ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Eukaryota/$UP_ID"_DNA.fasta.gz"
    curl -O ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Eukaryota/$UP_ID".gene2acc.gz"
    curl -O ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Eukaryota/$UP_ID".idmapping.gz"
  done
fi
