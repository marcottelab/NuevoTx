#!/usr/bin/env python3
import os
import sys

filename_input_best = 'XENTR_JGIv90pV2_prot_final.MODtree.treefam9.201806.bp+_tbl_best'
filename_input_fa = 'XENTR_JGIv90pV2_prot_final.fa'
dirname_output = './msa.XENTR'
filename_family_fa = '/home/taejoon/pub/MODtree/201806/MODtree.treefam9.201806.fa.gz'

f_fa = open(filename_family_fa,'r')
if filename_family_fa.endswith('.gz'):
    import gzip
    f_fa = gzip.open(filename_family_fa,'rt')

family2seq = dict()
family_seq_list = dict()
for line in f_fa:
    if line.startswith('>'):
        seq_h = line.strip().lstrip('>')
        family_seq_list[seq_h] = ''

        tmp_family_id = seq_h.split('|')[0]
        if not tmp_family_id in family2seq:
            family2seq[tmp_family_id] = []
        family2seq[tmp_family_id].append(seq_h)
    else:
        family_seq_list[seq_h] += line.strip()
f_fa.close()

input_seq_list = dict()
f_in_fa = open(filename_input_fa,'r')
for line in f_in_fa:
    if line.startswith('>'):
        seq_h = line.strip().lstrip('>')
        input_seq_list[seq_h] = []
    else:
        input_seq_list[seq_h].append( line.strip() )
f_in_fa.close()

#Qid	QLen	Tid	TLen	AlignLen	Mismatches	GapOpens	BitScore	Evalue
#42Sp43|Xetrov90024704m	366	TF333011|XENTR|42Sp43|ENSXETP00000059706	365	365	9	0	691.0	0.00e+00

family2input = dict()
f_best = open(filename_input_best,'r')
f_best.readline()
for line in f_best:
    tokens = line.strip().split("\t")
    family_id = tokens[2].split('|')[0]
    if not family_id in family2input:
        family2input[family_id] = []
    family2input[family_id].append(tokens[0])
f_best.close()

for tmp_family_id in family2input.keys():
    filename_output = os.path.join(dirname_output,'%s.msa_in.fa'%tmp_family_id)
    sys.stderr.write('Write %s\n'%filename_output)
    f_out = open(filename_output,'w')
    for tmp_id in family2input[tmp_family_id]:
        f_out.write('>%s\n%s\n'%(tmp_id, ''.join(input_seq_list[tmp_id])))

    for tmp_id in family2seq[tmp_family_id]:
        f_out.write('>%s\n%s\n'%(tmp_id, ''.join(family_seq_list[tmp_id])))
    f_out.close()
