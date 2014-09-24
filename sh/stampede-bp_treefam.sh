#!/bin/bash
#SBATCH -n 16
#SBATCH -p normal
#SBATCH -t 24:00:00
# #SBATCH --mail-type=ALL

BLASTP="$HOME/src/blast+/bin/blastp -evalue 1e0 -num_threads 16 -seg yes "

FA="YEAST_ens72_prot_annot_longest.fa"

#SBATCH -o bpTF9.o%j
#SBATCH -J "bpTF9.YEAST"

DB="$WORK/treefam/treefam9_rep.pin"

DB=${DB/.pin/}
DBNAME=$(basename $DB)
TBL=${FA/.fa/}"."$DBNAME".bp+E1_tbl"

time $BLASTP -db $DB -query $FA -out $TBL -outfmt "7 qseqid sseqid pident length mismatch gapopen qlen qstart qend slen sstart send evalue bitscore"

