#!/bin/bash
BLASTP="$HOME/git/NuevoTx/align/blastp -evalue 1e-4 -seg yes "

NUM_THREADS=8

FA=$1

DB="$HOME/pub/db.blast/MODtree.treefam9.201806.pin"
DB=${DB/.pin/}
DB_NAME=$(basename $DB)

OUT=${FA/.fa/}'.'$DB_NAME'.bp+_tbl'

echo $FA" --> "$OUT
time $BLASTP -db $DB -query $FA -out $OUT -num_threads $NUM_THREADS -outfmt "7 qseqid sseqid pident length mismatch gapopen qlen qstart qend slen sstart send evalue bitscore"

