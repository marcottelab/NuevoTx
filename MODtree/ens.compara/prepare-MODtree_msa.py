#!/usr/bin/env python3
import os
import sys

mtf_list = dict()
f_fa = open('MODtree_ens95_compara.fa', 'r')
for line in f_fa:
    if line.startswith('>'):
        tmp_h = line.strip()
        tokens = tmp_h.split()
        mtf_id = tokens[1]
        if mtf_id not in mtf_list:
            mtf_list[mtf_id] = dict()
        mtf_list[mtf_id][tmp_h] = []
    else:
        mtf_list[mtf_id][tmp_h].append(line.strip())
f_fa.close()

if not os.access('./msa/', os.R_OK):
    os.mkdir('./msa', mode=0o755)
for i in range(0,10):
    if not os.access('./msa/%d' % i, os.R_OK):
        os.mkdir('./msa/%d' % i, mode=0o755)

for mtf_id in mtf_list.keys():
    if len(mtf_list[mtf_id]) < 3:
        continue

    mtf_idx = int(mtf_id[-1])
    f_out = open('msa/%d/%s.msa_in.fa' % (mtf_idx, mtf_id), 'w')
    for tmp_h in sorted(mtf_list[mtf_id].keys()):
        f_out.write('%s\n%s\n' % (tmp_h, ''.join(mtf_list[mtf_id][tmp_h])))
    f_out.close()
