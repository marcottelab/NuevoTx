#!/usr/bin/env python3
import os
import sys
import gzip

max_t_list = 20
max_t_per_species = 5

filename_MODtree = \
    '/home/taejoon_kwon/git/NuevoTx/MODtree/MODtree.treefam9.201806.fa.gz'

filename_prot_targets = sys.argv[1]
filename_prot_fa = filename_prot_targets.replace('.prot_targets', '.prot.fa')
data_name = filename_prot_targets.split('.')[0]


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

dirname_msa = './msa.%s' % data_name
if not os.access(dirname_msa, os.W_OK):
    os.mkdir(dirname_msa, mode=0o755)

targets2query = dict()
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
            tmp_t_list[tmp_sp_id].append(t_id.split('=')[0])

    tmp_target_list = []
    for tmp_sp in tmp_t_list.keys():
        for tmp_t in tmp_t_list[tmp_sp]:
            tmp_target_list.append(tmp_t)

    tmp_target_str = ';'.join(sorted(tmp_target_list))
    if not tmp_target_str in targets2query:
        targets2query[tmp_target_str] = dict()
    targets2query[tmp_target_str][q_id] = best_bits
f_targets.close()

for tmp_t_str in targets2query.keys():
    count_q = 0
    tmp_t2q = targets2query[tmp_t_str]

    tmp_q_list = sorted(tmp_t2q.keys(), key=tmp_t2q.get, reverse=True)
    sys.stderr.write('Write %s\n' % tmp_q_list[0])
    f_out = open( os.path.join(dirname_msa, '%s.msa_in.fa' % tmp_q_list[0]), 'w')
    for tmp_q in tmp_q_list:
        count_q += 1
        f_out.write(">%s\n%s\n" % (tmp_q, qseq_list[tmp_q]))
        if count_q > 3:
            sys.stderr.write("Skipped: %s (%s\n" % (tmp_q, tmp_t_str.split(';')[1]))

    for tmp_t in tmp_t_str.split(';'):
        f_out.write(">%s\n%s\n" % (tmp_t, refseq_list[tmp_t]))
    f_out.close()

