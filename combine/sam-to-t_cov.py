#!/usr/bin/env python3
import sys

filename_sam = sys.argv[1]
filename_out = filename_sam.replace('.sam', '') + '.t_cov'

seq_cov = dict()
seq_len = dict()
f_sam = open(filename_sam, 'r')
for line in f_sam:
    if line.startswith('@SQ'):
        tokens = line.strip().split()
        tmp_seq_id = tokens[1].lstrip('SN:')
        tmp_seq_len = int(tokens[2].lstrip('LN:'))
        seq_cov[tmp_seq_id] = [0 for x in range(0, tmp_seq_len)]
        seq_len[tmp_seq_id] = tmp_seq_len
    elif not line.startswith('@'):
        tokens = line.strip().split("\t")
        tmp_seq_id = tokens[2]
        tmp_start = int(tokens[3])
        tmp_cigar = tokens[5]
        tmp_pair_id = tokens[6]
        if tmp_pair_id == '=' and tmp_cigar.rstrip('M').isdigit():
            tmp_pair_start = int(tokens[7])
            tmp_frag_start = min(tmp_start, tmp_pair_start)
            tmp_read_seq = tokens[9]
            tmp_frag_end = max(tmp_start, tmp_pair_start) + len(tmp_read_seq)
            tmp_frag_end = min(tmp_frag_end, seq_len[tmp_seq_id])
            # print(tmp_seq_id, tmp_start, tmp_pair_start,
            #       tmp_frag_start, tmp_frag_end, seq_len[tmp_seq_id])
            for i in range(tmp_frag_start-1, tmp_frag_end-1):
                seq_cov[tmp_seq_id][i] += 1
f_sam.close()

f_t_cov = open(filename_out, 'w')
for tmp_id in sorted(seq_cov.keys()):
    tmp_cov = (seq_len[tmp_id] - seq_cov[tmp_id].count(0)) / seq_len[tmp_id]
    if tmp_cov > 0:
        f_t_cov.write('%.3f\t%d\t%s\n' %
                      (tmp_cov * 100, seq_len[tmp_id], tmp_id))
f_t_cov.close()
