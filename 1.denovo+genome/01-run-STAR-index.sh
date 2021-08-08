#!/bin/bash

# Install STAR using conda
# $ conda install -c bioconda STAR

NUM_THREADS=8

DB_FASTA="GRCm39.primary_assembly.genome.fa"
DB_GTF="gencode.vM26.primary_assembly.annotation.gtf"
DB_DIR="db.STAR"

STAR --runThreadN $NUM_THREADS --runMode genomeGenerate --genomeDir $DB_DIR \
  --genomeFastaFiles $DB_FASTA --sjdbGTFfile $DB_GTF --sjdbOverhang 100
