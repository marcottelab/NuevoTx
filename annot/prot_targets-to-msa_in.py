#!/usr/bin/env python3
import os
import sys
import gzip

max_t_list = 20
max_t_per_species = 5

filename_MODtree = \
    '/home/taejoon/data/pub/MODtree/201806/MODtree.treefam9.201806.fa.gz'

filename_prot_targets = sys.argv[1]
filename_prot_fa = filename_prot_targets.replace('.prot_targets', '.prot.fa')


def open_file(tmp_filename):
    if tmp_filename.endswith('.gz'):
        return gzip.open(tmp_filename, 'rt')
    return open(tmp_filename, 'r')


refseq_list = dict()
seq_h = ''
f_MODtree = open_file(filename_MODtree)
for line in f_MODtree:
    if line.startswith('>'):
        seq_h = line.strip().lstrip('>')
        pf_id = seq_h.split('|')[0]
        refseq_list[seq_h] = ''
    else:
        refseq_list[seq_h] += line.strip()
f_MODtree.close()

qseq_list = dict()
f_prot_fa = open_file(filename_prot_fa)
for line in f_prot_fa:
    if line.startswith('>'):
        seq_h = line.strip().lstrip('>')
        qseq_list[seq_h] = ''
    else:
        qseq_list[seq_h] += line.strip()
f_prot_fa.close()

dirname_msa = './msa'
if not os.access(dirname_msa, os.W_OK):
    os.mkdir(dirname_msa, mode=755)

f_targets = open_file(filename_prot_targets)
for line in f_targets:
    tokens = line.strip().split("\t")

    q_id = tokens[0]
    best_bits = float(tokens[1])

    tmp_t_list = dict()
    for t_id in tokens[2].split(';'):
        tmp_pf_id = t_id.split('|')[0]
        tmp_sp_id = t_id.split('|')[1]
        if tmp_sp_id not in tmp_t_list:
            tmp_t_list[tmp_sp_id] = []
        if len(tmp_t_list[tmp_sp_id]) < max_t_per_species:
            tmp_t_list[tmp_sp_id].append(t_id)

    # pf_list = list(set([t_id.split('|')[0] for t_id in t_list]))
    # sp_list = list(set([t_id.split('|')[1] for t_id in t_list]))
    # t_count = len(t_list)
    # pf_count = len(pf_list)
    # sp_count = len(sp_list)
    # print(q_id, pf_count, sp_count, t_count)

    sys.stderr.write('Write %s\n' % q_id)
    f_out = open( os.path.join(dirname_msa, '%s.fa' % q_id), 'w')
    f_out.write(">%s\n%s\n" % (q_id, ''.join(qseq_list[q_id])))
f_targets.close()
