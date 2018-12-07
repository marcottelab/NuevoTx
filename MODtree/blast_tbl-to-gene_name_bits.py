#!/usr/bin/env python3
import sys
import gzip

filename_tbl = sys.argv[1]

name_bits = dict()
f_tbl = open(filename_tbl, 'r')
if filename_tbl.endswith('.gz'):
    f_tbl = gzip.open(filename_tbl, 'rt')

for line in f_tbl:
    if line.startswith('#'):
        continue

    tokens = line.strip().split("\t")
    q_name = tokens[0].split('|')[2].upper()
    t_name = tokens[1].split('|')[2].upper()
    tmp_bits = float(tokens[-1])

    if q_name == t_name:
        if q_name not in name_bits:
            name_bits[q_name] = []
        name_bits[q_name].append(tmp_bits)
f_tbl.close()

for tmp_name in sorted(name_bits.keys()):
    tmp_bits_list = sorted(name_bits[tmp_name])
    print("%s\t%.1f\t%.1f" % (tmp_name, tmp_bits_list[0], tmp_bits_list[-1]))
