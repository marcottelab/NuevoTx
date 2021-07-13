#!/usr/bin/env python3
import gzip
import os
import sys

filename_tx = sys.argv[1]
filename_base = filename_tx.split('.')[0]

rc = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N': 'N'}


def revcomp(tmp_seq):
    return ''.join([rc[x] for x in tmp_seq[::-1]])


seq_list = dict()
f_tx = open(filename_tx, 'r')
if filename_tx.endswith('.gz'):
    f_tx = gzip.open(filename_tx, 'rt')

for line in f_tx:
    if line.startswith('>'):
        tmp_h = line.strip().lstrip('>')
        tmp_id = tmp_h.split()[0]
        seq_list[tmp_id] = {'h': tmp_h, 'seqs': []}
    else:
        seq_list[tmp_id]['seqs'].append(line.strip())
f_tx.close()

q_best = dict()
t_best = dict()
for tmp_filename in os.listdir('.'):
    if tmp_filename.startswith(filename_base):
        if tmp_filename.find('.dmnd_bx_tbl6') >= 0:
            f = open(tmp_filename, 'r')
            if tmp_filename.endswith('.gz'):
                f = gzip.open(tmp_filename, 'rt')
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
                    q_best[q_id] = {'t_id': t_id, 'bits': tmp_bits,
                                    'q_start': q_start, 'q_end': q_end}
                elif tmp_bits > q_best[q_id]['bits']:
                    q_best[q_id] = {'t_id': t_id, 'bits': tmp_bits,
                                    'q_start': q_start, 'q_end': q_end}

                if t_id not in t_best:
                    t_best[t_id] = {'q_id': q_id, 'bits': tmp_bits,
                                    't_start': t_start, 't_end': t_end}
                elif tmp_bits > t_best[t_id]['bits']:
                    t_best[t_id] = {'q_id': q_id, 'bits': tmp_bits,
                                    't_start': t_start, 't_end': t_end}
            f.close()

f_out = open('%s.tx.orient.fa' % filename_base, 'w')
for tmp_q_id, tmp_q in q_best.items():
    tmp_t_id = tmp_q['t_id']
    tmp_bits = tmp_q['bits']
    t_best_bits = t_best[tmp_t_id]['bits']

    tmp_seq = ''.join(seq_list[tmp_q_id]['seqs'])
    tmp_h = seq_list[tmp_q_id]['h']

    f_out.write(">%s bx_bits=%.1f t_id=%s\n" % (tmp_h, tmp_bits, tmp_t_id))
    if tmp_q['q_start'] < tmp_q['q_end']:
        f_out.write("%s\n" % tmp_seq)
    else:
        f_out.write("%s\n" % revcomp(tmp_seq))
f_out.close()
