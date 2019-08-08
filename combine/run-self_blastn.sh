#!/bin/bash

NUM_THREADS=4

CUR_DIR=$(dirname $0)
MKDB=$CUR_DIR"../blast/makeblastdb"
BLASTN=$CUR_DIR"../blast/blastn -task megablast -evalue 1e-4 -dust yes -max_target_seqs 10"
NRSEQ=$CUR_DIR"make-NR_nseq.py"

for FA in $(ls *.combined_nTx.fa)
do
  NR_FA=${FA/.fa/_NR.fa}
  if [ ! -e $NR_FA ]; then
    echo "Make $NR_FA"
    $NRSEQ $FA
  else
    echo "$NR_FA exists."
  fi

  DB=${NR_FA/.fa/}
  OUT=$DB'.self.mb+_tbl'
  
  if [ ! -e $DB".nin" ]; then
    echo "Make $DB"
    $MKDB -dbtype nucl -in $NR_FA -out $DB
  fi

  if [ ! -e $OUT ]; then
    time $BLASTN -db $DB -query $NR_FA -out $OUT -num_threads $NUM_THREADS -outfmt "7 qseqid sseqid pident length mismatch gapopen qlen qstart qend slen sstart send evalue bitscore"
  fi
done
