#!/usr/bin/env python3
import sys

filename_nTx = sys.argv[1]

filename_base = filename_nTx.split('.')[0]
filename_out = '%s.tx.raw.fa' % filename_base

filename_kallisto = sys.argv[2]

exp_list = dict()
f_kallisto = open(filename_kallisto, 'r')
f_kallisto .readline()
for line in f_kallisto:
    tokens = line.strip().split("\t")
    exp_list[tokens[0]] = float(tokens[-1])
f_kallisto.close()

seq_list = dict()
seq_len = dict()
f_nTx = open(filename_nTx, 'r')
for line in f_nTx:
    if line.startswith('>'):
        tmp_h = line.strip().lstrip('>').split()[0]
        seq_list[tmp_h] = []
        seq_len[tmp_h] = 0
    else:
        seq_list[tmp_h].append(line.strip())
        seq_len[tmp_h] += len(line.strip())
f_nTx.close()

idx = 1
count_total = 0
count_pass = 0
f_out = open(filename_out, 'w')
for tmp_h in sorted(seq_len.keys(), key=seq_len.get, reverse=True):
    count_total += 1
    if exp_list[tmp_h] >= 0.01:
        count_pass += 1
        f_out.write('>%s.%07d len=%d tpm=%.2f\n' %
                    (filename_base, idx, seq_len[tmp_h], exp_list[tmp_h]))
        f_out.write('%s\n' % ''.join(seq_list[tmp_h]))
        idx += 1
f_out.close()

sys.stderr.write('Total input: %d\n' % count_total)
sys.stderr.write('Passed: %d (%.2f pct)\n' %
                 (count_pass, count_pass * 100.0 / count_total))
