#!/usr/bin/env python3
import sys
import gzip
import re

filename_tbl = sys.argv[1]
filename_base = re.sub(r'.bp\+\_tbl.gz', '', filename_tbl)

blastp_Evalue_cutoff = 0.0001
min_best_targets = 3


def open_file(tmp_filename):
    f = open(tmp_filename, 'r')
    if tmp_filename.endswith('.gz'):
        f = gzip.open(tmp_filename, 'rt')
    return f


blastp_list = dict()
sys.stderr.write('Read %s\n' % filename_tbl)
f_bp = open_file(filename_tbl)
for line in f_bp:
    if line.startswith('#'):
        continue

    tokens = line.strip().split("\t")
    q_id = tokens[0]
    t_id = tokens[1]
    evalue = float(tokens[-2])
    bits = float(tokens[-1])

    if evalue > blastp_Evalue_cutoff:
        continue

    if q_id not in blastp_list:
        blastp_list[q_id] = dict()

    if t_id not in blastp_list[q_id]:
        blastp_list[q_id][t_id] = bits
    elif bits > blastp_list[q_id][t_id]:
        blastp_list[q_id][t_id] = bits
f_bp.close()
sys.stderr.write('Total Sequences: %d\n' % len(blastp_list))

f_prot_targets = open('%s.prot_targets' % filename_base, 'w')
for tmp_h in blastp_list.keys():
    tmp_best_bits = max(blastp_list[tmp_h].values())
    tmp_target_list = \
                sorted(blastp_list[tmp_h].keys(), key=blastp_list[tmp_h].get, reverse=True)
    tmp_target_str = ';'.join(["%s=%.1f" % (x, blastp_list[tmp_h][x]) for x in tmp_target_list])
    f_prot_targets.write('%s\t%.1f\t%s\n' % (tmp_h, tmp_best_bits, tmp_target_str))
f_prot_targets.close()
