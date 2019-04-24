#!/usr/bin/env python3
import os
import sys
import gzip

filename_prot_targets = sys.argv[1]
data_name = filename_prot_targets.split('.')[0]
filename_out = filename_prot_targets.replace('.prot_targets','')
filename_out += '.prot_names'
min_sp_count = 2


ref_bits = dict()
filename_ref_bits = '/home/taejoon/git/NuevoTx/MODtree/MODtree.treefam9.201806.gene_name_bits'
f_ref_bits = open(filename_ref_bits, 'r')
for line in f_ref_bits:
    tokens = line.strip().split("\t")
    ref_bits[tokens[0]] = {'max': float(tokens[1]), 'min': float(tokens[3])}
f_ref_bits.close()


def open_file(tmp_filename):
    if tmp_filename.endswith('.gz'):
        return gzip.open(tmp_filename, 'rt')
    return open(tmp_filename, 'r')


f_out = open(filename_out, 'w')
f_out.write("#SeqID\tBestName\tBestBits\tHsName\tHsBits\tNumSpecies\tTargetList\n")

f_targets = open_file(filename_prot_targets)
for line in f_targets:
    tokens = line.strip().split("\t")

    q_id = tokens[0]
    best_bits = float(tokens[1])
    t_list_str = tokens[2]

    hs_best_name = 'NoName'
    hs_best_bits = 0

    tmp_name_list = dict()
    for t_id in t_list_str.split(';'):
        tmp_pf_id = t_id.split('|')[0]
        tmp_sp_id = t_id.split('|')[1]
        tmp_name = t_id.split('|')[2].upper().split('_')[0]
        tmp_bits = float(t_id.split('=')[1])

        if tmp_bits < best_bits * 0.4:
            continue
        
        if tmp_name not in tmp_name_list:
            tmp_name_list[tmp_name] = dict()

        if tmp_sp_id not in tmp_name_list[tmp_name]:
            tmp_name_list[tmp_name][tmp_sp_id] = {'bits':tmp_bits, 'id':t_id, 'pf':tmp_pf_id}
        
        if tmp_sp_id == 'HUMAN':
            if hs_best_name == 'NoName':
                hs_best_name = tmp_name
                hs_best_bits = tmp_bits
            elif tmp_bits > hs_best_bits:
                hs_best_name = tmp_name
                hs_best_bits = tmp_bits
    
    noname_str = 'NoName-%s' % (t_list_str.split('|')[0])
    best_name = noname_str
    best_sp_count = 0
    best_mean_bits = 0
    for tmp_name in tmp_name_list.keys():
        tmp_sp_count = len(tmp_name_list[tmp_name])
        if tmp_sp_count <= min_sp_count:
            continue
        
        if tmp_name not in ref_bits:
            continue

        max_ref_bits = ref_bits[tmp_name]['max']
        min_ref_bits = ref_bits[tmp_name]['min']

        tmp_mean_bits = sum([tmp_name_list[tmp_name][tmp_s]['bits'] for tmp_s in tmp_name_list[tmp_name].keys()]) / tmp_sp_count

        if tmp_mean_bits > min_ref_bits:
            if tmp_mean_bits > best_mean_bits:
                best_name = tmp_name
                best_mean_bits = tmp_mean_bits
                best_sp_count = tmp_sp_count
        elif tmp_mean_bits > best_mean_bits:
            best_name = '%s.%s' % (noname_str, tmp_name)
            best_mean_bits = tmp_mean_bits
            best_sp_count = tmp_sp_count

    f_out.write("%s\t%s\t%.1f\t%s\t%.2f\t%d\t%s\n" % (q_id, best_name, best_bits, hs_best_name, hs_best_bits, best_sp_count, t_list_str))
f_targets.close()
f_out.close()
