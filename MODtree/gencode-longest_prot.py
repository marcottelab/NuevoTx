#!/usr/bin/env python3
import sys
import gzip

filename_fa = sys.argv[1]

f_fa = open(filename_fa, 'r')
if filename_fa.endswith('.gz'):
    f_fa = gzip.open(filename_fa, 'rt')

seq_list = dict()
seqlen_list = dict()
for line in f_fa:
    if line.startswith('>'):
        tmp_tokens = line.strip().lstrip('>').split('|')
        tmp_gene_id = tmp_tokens[2]
        tmp_prot_id = tmp_tokens[0]
        tmp_gene_name = tmp_tokens[-2]
        tmp_seqlen = int(tmp_tokens[-1])

        tmp_species = 'Unknown'
        if tmp_gene_id.startswith('ENSG0'):
            tmp_species = 'HUMAN'
        if tmp_gene_id.startswith('ENSMUSG0'):
            tmp_species = 'MOUSE'

        tmp_gene = '%s|%s' % (tmp_species, tmp_gene_name)
        if tmp_gene not in seq_list:
            seq_list[tmp_gene] = dict()
            seqlen_list[tmp_gene] = dict()
        seqlen_list[tmp_gene][tmp_prot_id] = tmp_seqlen

        seq_list[tmp_gene][tmp_prot_id] = []
    else:
        seq_list[tmp_gene][tmp_prot_id].append(line.strip())
f_fa.close()

for tmp_gene in seq_list.keys():
    tmp_prot_id_list = sorted(seqlen_list[tmp_gene].keys(),
                              key=seqlen_list[tmp_gene].get)
    max_prot_id = tmp_prot_id_list[-1]
    print(">GENCODE|%s|%s\n%s" %
          (tmp_gene, max_prot_id, '\n'.join(seq_list[tmp_gene][max_prot_id])))
