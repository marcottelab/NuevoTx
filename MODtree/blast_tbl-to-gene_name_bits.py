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

    if q_name == t_name and tokens[0] != tokens[1]:
        if q_name not in name_bits:
            name_bits[q_name] = dict()

        pair_id = '%s-%s' % (tokens[0], tokens[1])
        if pair_id not in name_bits[q_name]:
            name_bits[q_name][pair_id] = tmp_bits
        elif tmp_bits > name_bits[q_name][pair_id]:
            name_bits[q_name][pair_id] = tmp_bits
f_tbl.close()

for tmp_name in sorted(name_bits.keys()):
    tmp_pair_list = sorted(name_bits[tmp_name].keys(), key=name_bits[tmp_name].get)
    min_bits_pair = tmp_pair_list[0]
    min_bits = name_bits[tmp_name][min_bits_pair]
    max_bits_pair = tmp_pair_list[-1]
    max_bits = name_bits[tmp_name][max_bits_pair]
    print("%s\t%.1f\t%s\t%.1f\t%s" %
          (tmp_name, max_bits, max_bits_pair, min_bits, min_bits_pair))
