#!/bin/bash
DB="MODtree_eggNOG50.Metazoa.raw.dmnd"
#DB="MODtree_eggNOG50.Vertebrata.raw.dmnd"
#MODtree_ens100.raw.dmnd

OUT_SUFFIX=${DB/.raw.dmnd/}
OUT_SUFFIX=${OUT_SUFFIX/\./_}".dmnd_bp_out"
echo $OUT_SUFFIX

QUERY_FA="GENCODE_HUMAN_pep_longest.r37.fa"
OUT=${QUERY_FA/.fa/}"."$OUT_SUFFIX
diamond blastp --query $QUERY_FA --outfmt 6 -b4 --db $DB --out $OUT

QUERY_FA="GENCODE_MOUSE_pep_longest.vM26.fa"
OUT=${QUERY_FA/.fa/}"."$OUT_SUFFIX
diamond blastp --query $QUERY_FA --outfmt 6 -b4 --db $DB --out $OUT
