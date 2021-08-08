#!/usr/bin/env python3
import gzip
import sys

# Downloaded from EggNOG site & gzipped first.
# http://eggnog5.embl.de/download/eggnog_5.0/e5.sequence_aliases.tsv
# Make it by zgrep 'BLAST_UniProt_GN' e5.sequence_aliases.tsv.gz

filename_in = 'e5.sequence_aliases.BLAST_UniProt_GN.tsv.gz'
filename_out = 'MODtree.ENOG50.gene_names.tsv'

filename_species = '/home/taejoon/git/NuevoTx/MODtree/MODtree_species.txt'
# UniProt_ID	UP_taxId	EN_taxId	sp_code	sp_name	GOA_name
# UP000005640	9606	9606	HUMAN	homo_sapiens	25.H_sapiens.goa

species_list = dict()
f_species = open(filename_species, 'r')
for line in f_species:
    if line.startswith('#'):
        continue
    tokens = line.strip().split("\t")
    tax_id = tokens[2]
    sp_code = tokens[3]
    species_list[tax_id] = sp_code
f_species.close()

f_out = open(filename_out, 'w')

sys.stderr.write('Read gene names...')
# 9541.XP_005587739.1	RFX2	BLAST_KEGG_NAME BLAST_UniProt_GN RefSeq_gene
f_GN = gzip.open(filename_in, 'rt')
for line in f_GN:
    tokens = line.strip().split("\t")
    seq_id = tokens[0]
    tax_id = seq_id.split('.')[0]
    if tax_id in species_list:
        f_out.write('%s\n' % line.strip())
f_GN.close()
sys.stderr.write('Done.\n')
f_out.close()
