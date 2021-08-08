#!/usr/bin/env python3
import os
import sys
import gzip

filename_family_fa = sys.argv[1]
dirname_output = sys.argv[2]

f_fa = open(filename_family_fa, 'r')
if filename_family_fa.endswith('.gz'):
    f_fa = gzip.open(filename_family_fa, 'rt')

family2seq = dict()
family_seq_list = dict()
for line in f_fa:
    if line.startswith('>'):
        seq_h = line.strip().lstrip('>')
        family_seq_list[seq_h] = ''

        tmp_family_id = seq_h.split('|')[0]
        if tmp_family_id not in family2seq:
            family2seq[tmp_family_id] = []
        family2seq[tmp_family_id].append(seq_h)
    else:
        family_seq_list[seq_h] += line.strip()
f_fa.close()

for tmp_family_id, tmp_h_list in family2seq.items():
    dirname_output_sub = os.path.join(dirname_output, tmp_family_id[-1])
    if not os.access(dirname_output_sub, os.W_OK):
        os.mkdir(dirname_output_sub)

    dirname_output_gt100 = os.path.join(dirname_output, 'gt100')
    if not os.access(dirname_output_gt100, os.W_OK):
        os.mkdir(dirname_output_gt100)

    dirname_output_lt3 = os.path.join(dirname_output, 'lt3')
    if not os.access(dirname_output_lt3, os.W_OK):
        os.mkdir(dirname_output_lt3)

    seq2h = dict()
    for tmp_id in sorted(tmp_h_list):
        ## Remove family_id from the sequence for display.
        new_id = tmp_id.replace('%s|' % tmp_family_id, '')
        tmp_seq = ''.join(family_seq_list[tmp_id]).replace('-', '')
        if tmp_seq not in seq2h:
            seq2h[tmp_seq] = []
        seq2h[tmp_seq].append(new_id)
    
    out_list = []
    for tmp_seq, tmp_h_list in seq2h.items():
        if len(tmp_h_list) == 1:
            out_list.append('>%s\n%s' % (tmp_h_list[0], tmp_seq))
        else:
            gencode_h_list = [x for x in tmp_h_list if x.endswith('-GENCODE')]
            if len(gencode_h_list) == 1:
                out_list.append('>%s\n%s' % (gencode_h_list[0], tmp_seq))
                for tmp_h in tmp_h_list:
                    if tmp_h == gencode_h_list[0]:
                        continue
                    sys.stderr.write('Replace %s --> %s (identical)\n' % (tmp_h, gencode_h_list[0]))
            else:
                out_list.append('>%s\n%s' % (tmp_h_list[0], tmp_seq))
                for tmp_h in tmp_h_list:
                    if tmp_h == tmp_h_list[0]:
                        continue
                    sys.stderr.write('Replace %s --> %s (identical)\n' % (tmp_h, tmp_h_list[0]))

    
    if len(out_list) > 100 * 2:
        filename_output = os.path.join(dirname_output_gt100,
                                       '%s.msa_in.fa' % tmp_family_id)
    elif len(out_list) < 3 * 2:
        filename_output = os.path.join(dirname_output_lt3,
                                       '%s.msa_in.fa' % tmp_family_id)
    else:
        filename_output = os.path.join(dirname_output_sub,
                                       '%s.msa_in.fa' % tmp_family_id)

    sys.stderr.write('Write %s\n' % filename_output)
    f_out = open(filename_output, 'w')
    f_out.write('\n'.join(out_list) + "\n")
    f_out.close()
