#!/bin/bash
#SBATCH -n 16
#SBATCH -p normal
#SBATCH -t 24:00:00

BLASTP="$HOME/src/blast+/bin/blastp -evalue 1e0 -num_threads 16 -seg yes -num_descriptions 16 -num_alignments 16 "

#SBATCH -o bpEN.o%j
#SBATCH -J "bpEN.ANOCA"

FA="YEAST_ens72_prot_annot_longest.fa"

DB="$WORK/eggNOG/eggnogv4_all_rep.pin"
#DB="$WORK/eggNOG/eggnogv4_opiNOG_rep.pin"
#DB="$WORK/eggnog/eggnogv4_NOG_rep.pin"
#DB="$WORK/eggnog/eggnogv4_euNOG_rep.pin"
#DB="$WORK/eggnog/eggnogv4_biNOG_rep.pin"
#DB="$WORK/eggnog/eggnogv4_fuNOG_rep.pin"

DB=${DB/.pin/}
DBNAME=$(basename $DB)
TBL=${FA/.fa/}"."$DBNAME".bp+E1_tbl"
time $BLASTP -db $DB -query $FA -out $TBL -outfmt "7 qseqid sseqid pident length mismatch gapopen qlen qstart qend slen sstart send evalue bitscore"

