#!/usr/bin/env python3
import sys
import gzip

filename_MODtree = \
    '/home/taejoon/data/pub/MODtree/201806/MODtree.treefam9.201806.fa.gz'
filename_prot_targets = sys.argv[1]


def open_file(tmp_filename):
    if tmp_filename.endswith('.gz'):
        return gzip.open(tmp_filename, 'rt')
    return open(tmp_filename, 'r')


refseq_list = dict()
pf_count_list = dict()

seq_h = ''
f_MODtree = open_file(filename_MODtree)
for line in f_MODtree:
    if line.startswith('>'):
        seq_h = line.strip().lstrip('>')
        pf_id = seq_h.split('|')[0]
        if pf_id not in pf_count_list:
            pf_count_list[pf_id] = 0

        pf_count_list[pf_id] += 1
        refseq_list[seq_h] = ''
    else:
        refseq_list[seq_h] += line.strip()
f_MODtree.close()

f_targets = open_file(filename_prot_targets)
for line in f_targets:
    tokens = line.strip().split("\t")

    q_id = tokens[0]
    t_list = tokens[2].split(',')
    pf_list = list(set([t_id.split('|')[0] for t_id in t_list]))

    t_count = len(t_list)
    pf_count = len(pf_list)
    # print(q_id, tf_count, t_count)
f_targets.close()
