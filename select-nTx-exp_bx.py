#!/usr/bin/env python3
import os
import sys
import re

#filename_nTx = 'TKLab201706h_HYNQUtx_mmsX002+liver.spades.nTx.fa'
filename_nTx = sys.argv[1]

filename_base = filename_nTx.split('.')[0]
filename_out = '%s.tx.raw.fa' % filename_base

filename_kallisto = '%s.kallisto_quant/abundance.tsv' % re.sub(r'.fa$', '', filename_nTx)


rc = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N': 'N'}
def revcomp(tmp_seq):
    return ''.join([rc[x] for x in tmp_seq[::-1]])

def read_kallisto_tsv(tmp_filename):
    rv = dict()
    f = open(tmp_filename, 'r')
    f.readline()
    for line in f:
        tokens = line.strip().split("\t")
        rv[tokens[0]] = float(tokens[-1])
    f.close()
    return rv


exp_list = read_kallisto_tsv(filename_kallisto)

seq_list = dict()
f_nTx = open(filename_nTx, 'r')
for line in f_nTx:
    if line.startswith('>'):
        tmp_h = line.strip().lstrip('>')
        seq_list[tmp_h] = []
    else:
        seq_list[tmp_h].append(line.strip())
f_nTx.close()


q_best = dict()
t_best = dict()
for tmp_filename in os.listdir('.'):
    if tmp_filename.endswith('.dmnd_bx_tbl6') and tmp_filename.startswith(filename_base):
        f = open(tmp_filename, 'r')
        for line in f:
            tokens = line.strip().split("\t")
            q_id = tokens[0]
            t_id = tokens[1]
            q_start = int(tokens[6])
            q_end = int(tokens[7])
            t_start = int(tokens[8])
            t_end = int(tokens[9])

            tmp_bits = float(tokens[-1])
            if q_id not in q_best:
                q_best[q_id] = {'t_id': t_id, 'bits': tmp_bits, 'q_start': q_start, 'q_end': q_end}
            elif tmp_bits > q_best[q_id]['bits']:
                q_best[q_id] = {'t_id': t_id, 'bits': tmp_bits, 'q_start': q_start, 'q_end': q_end}
            
            if t_id not in t_best:
                t_best[t_id] = {'q_id': q_id, 'bits': tmp_bits}
            elif tmp_bits > t_best[t_id]['bits']:
                t_best[t_id] = {'q_id': q_id, 'bits': tmp_bits}
        f.close()

f_out = open(filename_out, 'w')
for tmp_q_id, tmp_q in q_best.items():
    tmp_t_id = tmp_q['t_id']
    tmp_bits = tmp_q['bits']
    t_best_bits = t_best[tmp_t_id]['bits']
    
    tmp_exp = exp_list[tmp_q_id]
    if tmp_exp == 0:
        continue
    
    f_out.write(">%s bits=%.1f exp=%.1f t_id=%s\n" % (tmp_q_id, tmp_bits, tmp_exp, tmp_t_id))

    tmp_seq = ''.join(seq_list[tmp_q_id])
    if tmp_q['q_start'] < tmp_q['q_end']:
        f_out.write("%s\n" % tmp_seq)
    else:
        f_out.write("%s\n" % revcomp(tmp_seq))
f_out.close()
