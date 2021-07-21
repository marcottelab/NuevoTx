#!/usr/bin/env python3
import gzip
import os
import sys

dirname_tx_raw = sys.argv[1]
species_name = sys.argv[2]

version_AB = '2021_07'
count_per_t = 2

count_total = 0

prot_list = dict()
t_list = dict()
for tmp_filename in os.listdir(dirname_tx_raw):

    if not tmp_filename.endswith('.prot.raw.fa.gz'):
        continue

    sys.stderr.write('Read %s\n' % tmp_filename)

    filename_prot = tmp_filename

    f_prot = gzip.open(os.path.join(dirname_tx_raw, filename_prot), 'rt')
    for line in f_prot:
        if line.startswith('>'):
            tmp_h = line.strip().lstrip('>')
            count_total += 1
            prot_list[tmp_h] = []
            for tmp in tmp_h.split():
                if tmp.startswith('bx_bits'):
                    tmp_bits = float(tmp.split('=')[1])
                if tmp.startswith('len'):
                    tmp_len = int(tmp.split('=')[1])
                if tmp.startswith('tpm'):
                    tmp_tpm = float(tmp.split('=')[1])
                if tmp.startswith('t_id'):
                    tmp_tid = tmp.split('=')[1]

            if tmp_tid not in t_list:
                t_list[tmp_tid] = dict()
            t_list[tmp_tid][tmp_h] = tmp_bits
        else:
            prot_list[tmp_h].append(line.strip())
    f_prot.close()

q_list = []
for tmp_tid, tmp_t in t_list.items():
    for tmp_q in sorted(tmp_t.keys(),
                        key=tmp_t.get,
                        reverse=True)[:count_per_t]:
        q_list.append(tmp_q)

q_list = sorted(list(q_list))
sys.stderr.write('Select %d sequences (total: %d)\n' %
                 (len(q_list), count_total))

f_out = open('%s.prot.select.%s.fa' % (species_name, version_AB), 'w')
for tmp_q in q_list:
    f_out.write('>%s\n%s\n' % (tmp_q, ''.join(prot_list[tmp_q])))
f_out.close()
