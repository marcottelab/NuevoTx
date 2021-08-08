#!/bin/bash

DIR_IN="./msa.eggNOG50_Vertebrata"

for TREE in $(ls $DIR_IN/?/*.fasttree.nw)
do
  ALN=${TREE/.fasttree.nw/}".mafft_out.fa"
  TXT_TREE=${TREE/.fasttree.nw/}".fasttree.ete3.txt"
  SVG_TREE=${TREE/.fasttree.nw/}".fasttree.ete3.svg"
  
  if [ ! -e $SVG_TREE ]; then
    echo $SVG_TREE
    xvfb-run ete3 view --image $SVG_TREE -t $TREE --alg $ALN
    ete3 view --text -t $TREE > $TXT_TREE
  fi
done

