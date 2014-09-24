#!/bin/bash
#$ -V                   # Inherit the submission environment
#$ -cwd                 # Start job in submission directory
#$ -j y                 # Combine stderr and stdout
#$ -o $JOB_NAME.o$JOB_ID
#$ -pe 12way 12
#$ -q normal
#$ -l h_rt=24:00:00     # Run time (hh:mm:ss)
#$ -M $EMAIL
#$ -m be                # Email at Begin and End of job
#$ -P hpc
set -x                  # Echo commands, use "set echo" with csh

#$ -N bpENo.K1

BLASTP="$HOME/src/blast+/bin/blastp -evalue 1e0 -num_threads 12 -num_alignments 16 -seg yes "

#FA="EncodeCaltech_K562Rep1_NoPart_nTx_prot6.fa"

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

