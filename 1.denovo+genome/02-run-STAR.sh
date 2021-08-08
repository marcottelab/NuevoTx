#!/bin/bash

NUM_THREADS=8

GENOME_DIR="<STAR DB DIR>"
DB_GTF="<GTF FILE>"

for FQ1 in $(ls ../fastq.tx2/*_trim_1P.gz)
do
  FQ2=${FQ1/_1P/_2P}
  OUT=$(basename $FQ1)
  OUT=${OUT/_trim_1P.gz/}"."
  STAR --genomeDir $GENOME_DIR --runThreadN $NUM_THREADS \
      --readFilesIn $FQ1 $FQ2 --readFilesCommand zcat \
      --outSAMtype BAM SortedByCoordinate  \
      --outFileNamePrefix $OUT \
      --limitBAMsortRAM 1000000000 \
      --sjdbGTFfile $DB_GTF \
      --sjdbOverhang 100
done
