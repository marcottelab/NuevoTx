#!/usr/bin/env python3
import os
import sys

filename_fa = sys.argv[1]
filename_part = sys.argv[2]

filename_base = filename_fa.split('.')[0]

usage_mesg = 'make-NoPart_nTx.py <.fa> <.part>'

if not os.access(filename_fa, os.R_OK):
    sys.stderr.write('%s is not available.\n%s\n' % (filename_fa, usage_mesg))
    sys.exit(1)

if not os.access(filename_part, os.R_OK):
    sys.stderr.write('%s is not available.\n' % (filename_part))
    sys.stderr.write('%s\n' % (usage_mesg))
    sys.exit(1)

seq_h = ''
seq_list = dict()
seqlen = dict()

f_fa = open(filename_fa, 'r')
for line in f_fa:
    if line.startswith('>'):
        seq_h = line.strip().lstrip('>').split()[0]
        seq_list[seq_h] = []
        seqlen[seq_h] = 0
    else:
        seq_list[seq_h].append(line.strip())
        seqlen[seq_h] += len(line.strip())
f_fa.close()

q2t = dict()
t2q = dict()
f_part = open(filename_part, 'r')
for line in f_part:
    tokens = line.strip().split("\t")
    q_id = tokens[0]
    q_len = int(tokens[1])
    t_id = tokens[2]
    t_len = int(tokens[3])

    if q_id not in q2t:
        q2t[q_id] = dict()

    q2t[q_id][t_id] = 1
    if t_id not in t2q:
        t2q[t_id] = dict()
    t2q[t_id][q_id] = 1
f_part.close()

is_part = dict()
f_out = open('%s_NoPart_nTx.fa' % filename_base, 'w')
for tmp_h in sorted(seqlen.keys(), key=seqlen.get, reverse=True):
    if tmp_h in is_part:
        continue

    if tmp_h in t2q:
        for tmp_q in t2q[tmp_h].keys():
            is_part[tmp_q] = 1

    tmp_seq = ''.join(seq_list[tmp_h])
    f_out.write('>%s\n%s\n' % (tmp_h, tmp_seq))
f_out.close()
