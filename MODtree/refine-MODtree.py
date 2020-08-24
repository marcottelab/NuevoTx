#!/usr/bin/env python3
import os
import sys

filename_fa = sys.argv[1]
filename_base = filename_fa.replace('.raw.fa', '')

min_members = 3
max_members = 200

f_fa = open(filename_fa,'r')
if filename_fa.endswith('.gz'):
    import gzip
    f_fa = gzip.open(filename_fa,'rt')

family2seq = dict()
seq_list = dict()
for line in f_fa:
    if line.startswith('>'):
        seq_h = line.strip().lstrip('>')
        seq_list[seq_h] = ''

        tmp_family_id = seq_h.split('|')[0]
        tmp_sp_id = seq_h.split('|')[1]

        if tmp_family_id not in family2seq:
            family2seq[tmp_family_id] = dict()

        if tmp_sp_id not in family2seq[tmp_family_id]:
            family2seq[tmp_family_id][tmp_sp_id] = []
        family2seq[tmp_family_id][tmp_sp_id].append(seq_h)
    else:
        seq_list[seq_h] += line.strip()
f_fa.close()

f_log = open('%s.refine.log' % filename_base, 'w')
f_out = open('%s.refine.fa' % filename_base, 'w')
for tmp_family_id in family2seq.keys():
    tmp_sp_count = len(family2seq[tmp_family_id])
    tmp_id_str = ';'.join( sorted(family2seq[tmp_family_id].keys()) )

    if tmp_sp_count == 1:
        f_log.write('SingleSpecies\t%s\t%s\n' % (tmp_family_id, tmp_id_str))
        continue

    elif tmp_sp_count == 2:
        f_log.write('TwoSpecies\t%s\t%s\n' % (tmp_family_id, tmp_id_str))
        continue
   
    sp_seqlen = dict()
    sp_count = dict()
    tmp_seq_count = 0
    for tmp_sp_id in family2seq[tmp_family_id].keys():
        if tmp_sp_id not in sp_seqlen:
            sp_seqlen[tmp_sp_id] = dict()
            sp_count[tmp_sp_id] = 0

        for tmp_seq_id in family2seq[tmp_family_id][tmp_sp_id]:
            sp_seqlen[tmp_sp_id][tmp_seq_id] = len(seq_list[tmp_seq_id])
            sp_count[tmp_sp_id] += 1
            tmp_seq_count += 1
    
    sp_count_list = sorted(sp_count.values(), reverse=True)
    median_sp_count = sp_count_list[ int(len(sp_count_list)*0.5) ]
    max_seq_count = min(30, median_sp_count * 1.5)

    for tmp_sp_id in sp_count.keys():
        if sp_count[tmp_sp_id] < max_seq_count:
            for tmp_seq_id in sorted(sp_seqlen[tmp_sp_id].keys(), key=sp_seqlen[tmp_sp_id].get, reverse=True):
                tmp_seq = seq_list[tmp_seq_id]
                f_out.write('>%s\n%s\n' % (tmp_seq_id, tmp_seq))

        else:
            tmp_count = 0
            for tmp_seq_id in sorted(sp_seqlen[tmp_sp_id].keys(), key=sp_seqlen[tmp_sp_id].get, reverse=True):
                tmp_count += 1
                if tmp_count < max_seq_count:
                    tmp_seq = seq_list[tmp_seq_id]
                    f_out.write('>%s\n%s\n' % (tmp_seq_id, tmp_seq))
                else:
                    f_log.write('TooMuchSpeciesSeq\t%s\t%s\n' % (tmp_family_id, tmp_seq_id))
f_log.close()
f_out.close()

