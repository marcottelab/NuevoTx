#!/usr/bin/env python3
import os
import sys
import gzip

filename_prot_targets = sys.argv[1]
data_name = filename_prot_targets.split('.')[0]
min_sp_count = 2


def open_file(tmp_filename):
    if tmp_filename.endswith('.gz'):
        return gzip.open(tmp_filename, 'rt')
    return open(tmp_filename, 'r')


f_targets = open_file(filename_prot_targets)
for line in f_targets:
    tokens = line.strip().split("\t")

    q_id = tokens[0]
    best_bits = float(tokens[1])
    t_list_str = tokens[2]

    tmp_name_list = dict()
    for t_id in t_list_str.split(';'):
        tmp_pf_id = t_id.split('|')[0]
        tmp_sp_id = t_id.split('|')[1]
        tmp_name = t_id.split('|')[2].upper().split('_')[0]
        #print(t_id)
        tmp_bits = float(t_id.split('=')[1])

        if tmp_bits < best_bits * 0.4:
            continue
        
        if tmp_name not in tmp_name_list:
            tmp_name_list[tmp_name] = dict()

        if tmp_sp_id not in tmp_name_list[tmp_name]:
            tmp_name_list[tmp_name][tmp_sp_id] = {'bits':tmp_bits, 'id':t_id, 'pf':tmp_pf_id}
    
    best_name = 'NoName-%s' % (t_list_str.split('|')[0])
    best_sp_count = 0
    best_mean_bits = 0
    for tmp_name in tmp_name_list.keys():
        tmp_sp_count = len(tmp_name_list[tmp_name])
        tmp_mean_bits = sum([tmp_name_list[tmp_name][tmp_s]['bits'] for tmp_s in tmp_name_list[tmp_name].keys()]) / tmp_sp_count
        if tmp_mean_bits > best_mean_bits and tmp_sp_count > min_sp_count:
            best_name = tmp_name
            best_mean_bits = tmp_mean_bits
            best_sp_count = tmp_sp_count

    print("%s\t%.1f\t%s\t%d\t%s" % (q_id, best_bits, best_name, best_sp_count, t_list_str))
f_targets.close()
