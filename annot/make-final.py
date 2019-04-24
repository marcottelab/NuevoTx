#!/usr/bin/env python3
import sys
import re

filename_prot_names = sys.argv[1]

filename_base = filename_prot_names.split('.')[0]
filename_prot_fa = '%s.prot.fa' % filename_base
filename_cdna_fa = '%s.cdna.fa' % filename_base

ref_bits = dict()

dirname_script = '/home/taejoon/git/NuevoTx/MODtree/'
filename_ref_bits = dirname_script + '/MODtree.treefam9.201806.gene_name_bits'


def read_fasta(tmp_filename):
    seq_list = dict()
    seq_h = ''
    f = open(tmp_filename, 'r')
    for line in f:
        if line.startswith('>'):
            seq_h = line.strip().lstrip('>')
            seq_list[seq_h] = []
        else:
            seq_list[seq_h].append(line.strip())
    f.close()
    return seq_list


cdna_seq_list = read_fasta(filename_cdna_fa)
prot_seq_list = read_fasta(filename_prot_fa)

f_ref_bits = open(filename_ref_bits, 'r')
for line in f_ref_bits:
    tokens = line.strip().split("\t")
    gene_name = tokens[0]
    max_bits = float(tokens[1])
    min_bits = float(tokens[3])
    ref_bits[gene_name] = {'min': min_bits, 'max': max_bits}
f_ref_bits.close()

full_list = dict()
partial_list = dict()
noname_list = dict()

f_list = open(filename_prot_names, 'r')
for line in f_list:
    if line.startswith('#'):
        continue

    line = line.strip()
    tokens = line.split("\t")
    q_prot_id = tokens[0]
    q_tx_id = re.sub(r'^p.', 't.', q_prot_id)
    tmp_name = tokens[3]
    best_bits = float(tokens[4])

    if tmp_name in ref_bits:
        if best_bits > ref_bits[tmp_name]['min']:
            if tmp_name not in full_list:
                full_list[tmp_name] = {'bits': best_bits, 'p': q_prot_id, 't': q_tx_id}
            elif best_bits > full_list[tmp_name]['bits']:
                full_list[tmp_name] = {'bits': best_bits, 'p': q_prot_id, 't': q_tx_id}
        else:
            if tmp_name not in partial_list:
                partial_list[tmp_name] = {'bits': best_bits, 'p': q_prot_id, 't': q_tx_id}
            elif best_bits > partial_list[tmp_name]['bits']:
                partial_list[tmp_name] = {'bits': best_bits, 'p': q_prot_id, 't': q_tx_id}
    else:
        if tmp_name not in noname_list:
            noname_list[tmp_name] = {'bits': best_bits, 'p': q_prot_id, 't': q_tx_id}
        elif best_bits > noname_list[tmp_name]['bits']:
            noname_list[tmp_name] = {'bits': best_bits, 'p': q_prot_id, 't': q_tx_id}

f_list.close()

count_full = len(full_list)
count_noname = len(noname_list)
count_partial = len([x for x in partial_list.keys() if x not in full_list])
count_total = count_full + count_partial + count_noname

sys.stderr.write('Full: %d, Partial: %d, Noname: %d = Total: %d\n' %
                 (count_full, count_partial, count_noname, count_total))


cdna_final = open('%s.cdna_final.fa' % filename_base, 'w')
cds_final = open('%s.cds_final.fa' % filename_base, 'w')
prot_final = open('%s.prot_final.fa' % filename_base, 'w')

for tmp_name in full_list.keys():
    tmp_p_id = full_list[tmp_name]['p']
    tmp_t_id = full_list[tmp_name]['t']
    tmp_bits = full_list[tmp_name]['bits']
    min_bits = ref_bits[tmp_name]['min']
    max_bits = ref_bits[tmp_name]['max']

    cdna_final.write('>%s|%s FULL bits:%.1f min:%.1f max:%.1f\n' %
                     (tmp_name, tmp_t_id, tmp_bits, min_bits, max_bits))
    cdna_final.write('%s\n' % ''.join(cdna_seq_list[tmp_t_id]))
    prot_final.write('>%s|%s FULL bits:%.1f min:%.1f max:%.1f\n' %
                     (tmp_name, tmp_p_id, tmp_bits, min_bits, max_bits))
    prot_final.write('%s\n' % ''.join(prot_seq_list[tmp_p_id]))

for tmp_name in partial_list.keys():
    if tmp_name in full_list:
        continue

    tmp_p_id = partial_list[tmp_name]['p']
    tmp_t_id = partial_list[tmp_name]['t']
    tmp_bits = partial_list[tmp_name]['bits']
    min_bits = ref_bits[tmp_name]['min']
    max_bits = ref_bits[tmp_name]['max']

    cdna_final.write('>%s|%s PARTIAL bits:%.1f min:%.1f max:%.1f\n' %
                     (tmp_name, tmp_t_id, tmp_bits, min_bits, max_bits))
    cdna_final.write('%s\n' % ''.join(cdna_seq_list[tmp_t_id]))
    prot_final.write('>%s|%s PARTIAL bits:%.1f min:%.1f max:%.1f\n' %
                     (tmp_name, tmp_p_id, tmp_bits, min_bits, max_bits))
    prot_final.write('%s\n' % ''.join(prot_seq_list[tmp_p_id]))

for tmp_name in noname_list.keys():
    tmp_p_id = noname_list[tmp_name]['p']
    tmp_t_id = noname_list[tmp_name]['t']
    tmp_bits = noname_list[tmp_name]['bits']
    min_bits = 0.0
    max_bits = 0.0

    cdna_final.write('>%s|%s NONAME bits:%.1f min:%.1f max:%.1f\n' %
                     (tmp_name, tmp_t_id, tmp_bits, min_bits, max_bits))
    cdna_final.write('%s\n' % ''.join(cdna_seq_list[tmp_t_id]))
    prot_final.write('>%s|%s NONAME bits:%.1f min:%.1f max:%.1f\n' %
                     (tmp_name, tmp_p_id, tmp_bits, min_bits, max_bits))
    prot_final.write('%s\n' % ''.join(prot_seq_list[tmp_p_id]))


#for tmp_name in partial_list.keys():
#    if tmp_name not in full_list:
#        print(tmp_name)

#p.TKLab201809_KALBOtx_Lung_mms8591_paired.00000001	254.0	NoName-TF332233	0	TF332233|DANRE|CR388416.1|ENSDARP00000101155=254.0;TF332233|DANRE|CR936442.1|ENSDARP00000020392=253.0;TF332233|MOUSE|Syna|ENSMUSP00000116437=72.0;TF332233|HUMAN|ERVW-1|ENSP00000419945=49.7;TF332233|MOUSE|Synb|ENSMUSP00000061107=48.5

#for tmp_name in partial_list.keys():
#    if tmp_name not in full_list:
#        print(tmp_name)

#p.TKLab201809_KALBOtx_Lung_mms8591_paired.00000001	254.0	NoName-TF332233	0	TF332233|DANRE|CR388416.1|ENSDARP00000101155=254.0;TF332233|DANRE|CR936442.1|ENSDARP00000020392=253.0;TF332233|MOUSE|Syna|ENSMUSP00000116437=72.0;TF332233|HUMAN|ERVW-1|ENSP00000419945=49.7;TF332233|MOUSE|Synb|ENSMUSP00000061107=48.5
