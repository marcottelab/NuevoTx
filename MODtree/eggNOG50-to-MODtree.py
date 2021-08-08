#!/usr/bin/env python3
import os
import gzip
import sys

# Run this scrpipt under eggNOG 5.0 per_tax_level folder, 
# mirroring the following site.

# 33208_Metazoa
# http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/33208/

# 7742_Vertebrata
# http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/7742/

tax_list = {'Vertebrata': 7742, 'Metazoa': 33208}
tax_info = sys.argv[1] # either 'Vertebrata' or 'Metazoa'
if tax_info not in tax_list:
    sys.stderr.write('tax_info is missing.\n')
    sys.exit(1)

dirname_script = os.path.dirname(os.path.realpath(__file__))

dirname_output = 'MODtree_eggNOG50.%s.raw_alg' % tax_info
filename_out_base = 'MODtree_eggNOG50.%s' % tax_info

# Run under 33208_Metazoa with following file.
dirname_tax = '%d_%s' % (tax_list[tax_info], tax_info)
filename_members = '%d_members.tsv.gz' % tax_list[tax_info]
filename_members = os.path.join(dirname_tax, filename_members)

# Directory generated from 33208_raw_algs.tar
dirname_raw_alg = os.path.join(dirname_tax, '%d' % tax_list[tax_info])

# Make it by grep 'BLAST_UniProt_GN' e5.sequence_aliases.tsv
filename_GN = 'e5.sequence_aliases.BLAST_UniProt_GN.tsv.gz'

filename_species = os.path.join(dirname_script, 'MODtree_species.txt')
# UniProt_ID	UP_taxId	EN_taxId	sp_code	sp_name	GOA_name
# UP000005640	9606	9606	HUMAN	homo_sapiens	25.H_sapiens.goa

species_list = dict()
sys.stderr.write('Read %s ... ' % filename_species)
f_species = open(filename_species, 'r')
for line in f_species:
    if line.startswith('#'):
        continue
    tokens = line.strip().split("\t")
    tax_id = tokens[2]
    sp_code = tokens[3]
    species_list[tax_id] = sp_code
f_species.close()
sys.stderr.write('Done\n')

sys.stderr.write('Read gene names from %s...' % filename_GN)
gene_names = dict()
# 9541.XP_005587739.1	RFX2	BLAST_KEGG_NAME BLAST_UniProt_GN RefSeq_gene
f_GN = gzip.open(filename_GN, 'rt')
for line in f_GN:
    tokens = line.strip().split("\t")
    seq_id = tokens[0]
    tmp_name = tokens[1]

    # Refine the gene name
    # because of DANRE name like si:ch211-151m7.6
    tmp_name = tmp_name.replace(':', '_')
    tmp_name = tmp_name.replace(' ', '_')

    # because of CIOIN name like zf(cchc)-22
    tmp_name = tmp_name.replace('(', '_').replace(')', '_')
    tmp_name = tmp_name.replace('/', '_')

    tax_id = seq_id.split('.')[0]
    if tax_id in species_list:
        gene_names[seq_id] = tmp_name
f_GN.close()
sys.stderr.write('Done.\n')

family2seq = dict()
exclude_family = dict()
f_members = open(filename_members, 'r')
if filename_members.endswith('.gz'):
    f_members = gzip.open(filename_members, 'rt')

# In
# 7742	48URP	89	87	10029.XP_007630944.1,10036.XP_005064951.1,...
# Out
# E100F00001|ANOCA|NotAvail|ENSACAP00000018721	E100F00001	ENSACAP00000018721	ANOCA	NotAvail

new_headers = dict()
f_out_txt = open('%s.raw.txt' % filename_out_base, 'w')
for line in f_members:
    tokens = line.strip().split("\t")
    family_id = tokens[1]
    total_seqs = int(tokens[2])
    total_species = int(tokens[3])

    seq_list = []
    sp_code_list = []
    for tmp_id in tokens[4].split(','):
        tmp_tax_id = tmp_id.split('.')[0]
        tmp_prot_id = tmp_id.split('.')[1]
        if tmp_tax_id in species_list:
            tmp_sp_code = species_list[tmp_tax_id]
            tmp_gene_name = 'NotAvail'
            if tmp_id in gene_names:
                tmp_gene_name = gene_names[tmp_id]
            sp_code_list.append(tmp_sp_code)
            seq_list.append(tmp_id)
            seq_h = '%s|%s|%s|%s' % (family_id, tmp_sp_code,\
                                     tmp_gene_name, tmp_prot_id)
            new_headers[tmp_id] = seq_h
            f_out_txt.write('%s\t%s\t%s\t%s\t%s\n' % 
                            (seq_h, family_id, tmp_prot_id, 
                             tmp_sp_code, tmp_gene_name))

    count_seqs = len(seq_list)
    if count_seqs == 0:
        continue

    if count_seqs > 1:
        family2seq[family_id] = seq_list
f_members.close()
sys.stderr.write('Processed members.tsv.\n')

f_out_fa = open('%s.raw.fa' % filename_out_base, 'w')
for tmp_family_id, tmp_seq_list in family2seq.items():
    tmp_filename_fa = os.path.join(dirname_raw_alg,
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

    for tmp_seq_id in family2seq[tmp_family_id]:
        if tmp_seq_id not in tmp_seq_list:
            sys.stderr.write('%s has no sequences. (%s)\n' %
                             (tmp_seq_id, tmp_filename_fa))
            continue


        tmp_new_h = new_headers[tmp_seq_id]
        tmp_seq = ''.join(tmp_seq_list[tmp_seq_id])
        tmp_new_seq = tmp_seq.replace('-', '')

        f_out_fa.write('>%s\n%s\n' % (tmp_new_h, tmp_seq))
f_out_fa.close()
