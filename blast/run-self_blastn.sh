#!/bin/bash
#$ -V
#$ -cwd
#$ -j y
#$ -o $JOB_NAME.o$JOB_ID
#$ -pe 1way 12
#$ -q normal
#$ -l h_rt=24:00:00
#$ -M $EMAIL
#$ -m be
#$ -P hpc
set -x
#$ -N mbS.ENGPUs

MKDB="$HOME/git/NuevoTx/blast/makeblastdb"
BLASTN="$HOME/git/NuevoTx/blast/blastn -task megablast -evalue 1e-4 -num_threads 12 -dust yes "
NRSEQ="$HOME/git/HTseq-toolbox/oTx/make-NR_nseq.py"

FA="foobar.combined_nTx.fa"

DB=${FA/.fa/_NR}
OUT=$DB'.self.mb+_tbl'

$NRSEQ $FA
NR_FA=${FA/.fa/.NR_fa}

$MKDB -dbtype nucl -in $NR_FA -out $DB
time $BLASTN -db $DB -query $NR_FA -out $OUT -outfmt "7 qseqid sseqid pident length mismatch gapopen qlen qstart qend slen sstart send evalue bitscore"
$BEST $OUT
