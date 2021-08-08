#!/usr/bin/env python3
import os
import gzip
import sys

# Run this scrpipt under 33208_Vertebrate folder, mirroring the following site.
# http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/33208/

dirname_curr = os.path.dirname(os.path.realpath(__file__))
dirname_output = 'MODtree_ENOG50.raw_alg'
filename_out_base = 'MODtree_ENOG50'

# Run under 33208_Metazoa with following file.
filename_members = '33208_members.tsv.gz'

# Directory generated from 33208_raw_algs.tar
dirname_align = '33208'

# Make it by grep 'BLAST_UniProt_GN' e5.sequence_aliases.tsv
filename_GN = os.path.join(dirname_curr, 'MODtree_ENOG50.gene_names.tsv.gz')

filename_species = os.path.join(dirname_curr, 'MODtree_species.txt')
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

sys.stderr.write('Read gene names...')
gene_names = dict()
# 9541.XP_005587739.1	RFX2	BLAST_KEGG_NAME BLAST_UniProt_GN RefSeq_gene
f_GN = gzip.open(filename_GN, 'rt')
for line in f_GN:
    tokens = line.strip().split("\t")
    seq_id = tokens[0]
    tmp_name = tokens[1]
    tax_id = seq_id.split('.')[0]
    if tax_id in species_list:
        gene_names[seq_id] = tmp_name
f_GN.close()
sys.stderr.write('Done.\n')

f_out_members = open('%s.members.tsv' % filename_out_base, 'w')
f_out_members.write('# %s\t%s\t%s\t%s\t%s\t%s\n' %
                    ('EN_Id', 'TotalSpecies', 'TotalSeqs',
                     'MODtreeSpecies', 'MODtreeSeqs', 'MODtreeSpeciesList'))

family2seq = dict()
exclude_family = dict()
f_members = open(filename_members, 'r')
if filename_members.endswith('.gz'):
    f_members = gzip.open(filename_members, 'rt')
for line in f_members:
    tokens = line.strip().split("\t")
    family_id = tokens[1]
    total_seqs = int(tokens[2])
    total_species = int(tokens[3])

    seq_list = []
    sp_code_list = []
    for tmp_id in tokens[4].split(','):
        tmp_tax_id = tmp_id.split('.')[0]
        if tmp_tax_id in species_list:
            sp_code_list.append(species_list[tmp_tax_id])
            seq_list.append(tmp_id)

    count_seqs = len(seq_list)
    if count_seqs == 0:
        continue

    sp_code_list = sorted(list(set(sp_code_list)))
    count_species = len(sp_code_list)
    species_str = ','.join(sp_code_list)

    f_out_members.write('%s\t%d\t%d\t%d\t%d\t%s\n' %
                        (family_id, total_species, total_seqs,
                         count_species, count_seqs, species_str))
    if count_seqs > 1:
        family2seq[family_id] = seq_list

        if count_seqs > 150:
            exclude_family[family_id] = 1
f_members.close()
sys.stderr.write('Processed members.tsv.\n')


f_out_combined = open('%s.combined.faa' % filename_out_base, 'w')
for tmp_family_id in family2seq.keys():
    tmp_filename_fa = os.path.join(dirname_align,
                                   '%s.raw_alg.faa.gz' % tmp_family_id)

    tmp_seq_list = dict()
    f_fa = gzip.open(tmp_filename_fa, 'rt')
    for line in f_fa:
        if line.startswith('>'):
            tmp_h = line.strip().lstrip('>')
            tmp_seq_list[tmp_h] = []
        else:
            tmp_seq_list[tmp_h].append(line.strip())
    f_fa.close()

    tmp_filename_out = os.path.join(dirname_output,
                                    '%s.raw_alg.faa' % tmp_family_id)
    if tmp_family_id in exclude_family:
        tmp_filename_out = os.path.join('excluded_%s.raw_alg.faa' %
                                        tmp_family_id)

    f_fa_out = open(tmp_filename_out, 'w')
    for tmp_seq_id in family2seq[tmp_family_id]:
        tmp_tax_id = tmp_seq_id.split('.')[0]

        if tmp_seq_id not in tmp_seq_list:
            sys.stderr.write('%s has no sequences. (%s)\n' %
                             (tmp_seq_id, tmp_filename_fa))
            continue

        tmp_sp_code = species_list[tmp_tax_id]
        tmp_name = 'NotAvail'
        if tmp_seq_id in gene_names:
            tmp_name = gene_names[tmp_seq_id]

        # Refine the gene name
        # because of DANRE name like si:ch211-151m7.6
        tmp_name = tmp_name.replace(':', '_')
        tmp_name = tmp_name.replace(' ', '_')

        # because of CIOIN name like zf(cchc)-22
        tmp_name = tmp_name.replace('(', '_').replace(')', '_')
        tmp_name = tmp_name.replace('/', '_')

        tmp_id = tmp_seq_id.split('.')[1]
        tmp_new_h = '%s|%s|%s|%s' % (tmp_name, tmp_sp_code,
                                     tmp_family_id, tmp_id)
        tmp_seq = ''.join(tmp_seq_list[tmp_seq_id])
        tmp_new_seq = tmp_seq.replace('-', '')
        if tmp_family_id in exclude_family:
            tmp_new_h = '%s|excluded' % tmp_new_h
        f_fa_out.write('>%s\n%s\n' % (tmp_new_h, tmp_seq))
        f_out_combined.write('>%s\n%s\n' % (tmp_new_h, tmp_new_seq))
    f_fa_out.close()
f_out_combined.write
