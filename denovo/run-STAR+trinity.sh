#!/bin/bash
  
for BAM in $(ls ../STAR/*.sorted.bam)
do
  OUT=$(basename $BAM)
  OUT=${OUT/.STAR.sorted.bam/}".trinity"

  if [ ! -e $OUT ]; then
    echo "WORK "$OUT
    Trinity --genome_guided_bam $BAM  --output $OUT \
            --genome_guided_max_intron 10000 --max_memory 60G --CPU 14
  else
    echo "Skip "$OUT
  fi
done
