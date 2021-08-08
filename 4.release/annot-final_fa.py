#!/usr/bin/env python3
import sys
import gzip

filename_list = sys.argv[1]
filename_fa = sys.argv[2]
# tx, cds, prot
file_type = sys.argv[3]

selected = dict()

f_list = open(filename_list, 'r')
h_list = f_list.readline().strip().lstrip('#').split("\t")
tx_id_idx = h_list.index('tx_ID')
prot_id_idx = h_list.index('prot_ID')
gene_name_idx = h_list.index('gene_name')
orig_id_idx = h_list.index('orig_ID')
family_id_idx = h_list.index('family_ID')
family_class_idx = h_list.index('family_class')
for line in f_list:
    if line.startswith('#'):
        continue
    tokens = line.strip().split("\t")
    tx_id = tokens[tx_id_idx]
    prot_id = tokens[prot_id_idx]
    orig_id = tokens[orig_id_idx]
    gene_name = tokens[gene_name_idx]
    family_class = tokens[family_class_idx]
    family_id = tokens[family_id_idx]
    if file_type == 'prot':
        new_h = '%s|%s|%s %s %s' % \
                (gene_name, prot_id, family_id, family_class, orig_id)
    elif file_type == 'tx':
        new_h = '%s|%s|%s %s %s' % \
                (gene_name, tx_id, family_id, family_class, orig_id)
    elif file_type == 'cds':
        new_h = '%s|CDS.%s|%s %s %s' % \
                (gene_name, tx_id, family_id, family_class, orig_id)
    else:
        sys.stderr.write('Unknown file type: %s\n' % file_type)
        sys.exit(1)
    selected[orig_id] = new_h
f_list.close()


f_fa = open(filename_fa, 'r')
if filename_fa.endswith('.gz'):
    f_fa = gzip.open(filename_fa, 'rt')
for line in f_fa:
    if line.startswith('>'):
        tmp_id = line.strip().lstrip('>').split()[0]
        if tmp_id in selected:
            is_print = 1
            print(">%s" % selected[tmp_id])
        else:
            is_print = -1
    elif is_print > 0:
        print(line.strip())
f_fa.close()
