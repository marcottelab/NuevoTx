#!/usr/bin/env python3
import os
import sys
import gzip
import re

filename_nTx = sys.argv[1]
filename_base = re.sub(r'.fa(sta)*(.gz)*$', '', filename_nTx)
data_name = filename_base.split('_NoPart_nTx')[0]

frame_list = ['f0', 'f1', 'f2', 'r0', 'r1', 'r2']
hmmsearch_Evalue_cutoff = 0.1
blastp_Evalue_cutoff = 0.0001
min_best_targets = 3


def open_file(tmp_filename):
    f = open(tmp_filename, 'r')
    if tmp_filename.endswith('.gz'):
        f = gzip.open(tmp_filename, 'rt')
    return f


cdna_seq_list = dict()
prot_seq_list = dict()
hmmer_list = dict()
blastp_list = dict()
for tmp_filename in os.listdir('.'):
    if not tmp_filename.startswith(filename_base):
        continue

    # For nTX
    if tmp_filename == filename_nTx:
        sys.stderr.write('Read %s\n' % tmp_filename)
        f = open_file(tmp_filename)
        for line in f:
            if line.startswith('>'):
                tmp_h = line.strip().lstrip('>')
                cdna_seq_list[tmp_h] = []
            else:
                cdna_seq_list[tmp_h].append(line.strip())
        f.close()
        sys.stderr.write('Total Sequences: %d\n' % len(cdna_seq_list))

    # For nTX_prot6
    if tmp_filename.find('_prot6.fa') >= 0:
        sys.stderr.write('Read %s\n' % tmp_filename)
        f = open_file(tmp_filename)
        for line in f:
            if line.startswith('>'):
                tmp_h = line.strip().lstrip('>')
                prot_seq_list[tmp_h] = []
            else:
                prot_seq_list[tmp_h].append(line.strip())
        f.close()
        sys.stderr.write('Total Sequences: %d\n' % len(prot_seq_list))

    # For BLASTP output
    if tmp_filename.find('.bp+_tbl') >= 0 \
            and tmp_filename.find('MODtree') >= 0:
        sys.stderr.write('Read %s\n' % tmp_filename)
        f_bp = open_file(tmp_filename)
        for line in f_bp:
            if line.startswith('#'):
                continue

            tokens = line.strip().split("\t")
            q_id = tokens[0]
            q_tokens = q_id.split('|')
            seq_id = '|'.join(q_tokens[:-1])
            tmp_frame = q_tokens[-1]
            t_id = tokens[1]
            evalue = float(tokens[-2])
            bits = float(tokens[-1])

            if evalue > blastp_Evalue_cutoff:
                continue

            if seq_id not in blastp_list:
                blastp_list[seq_id] = dict()

            if tmp_frame not in blastp_list[seq_id]:
                blastp_list[seq_id][tmp_frame] = dict()

            if t_id not in blastp_list[seq_id][tmp_frame]:
                blastp_list[seq_id][tmp_frame][t_id] = bits
            elif bits > blastp_list[seq_id][tmp_frame][t_id]:
                blastp_list[seq_id][tmp_frame][t_id] = bits

        f_bp.close()
        sys.stderr.write('Total Sequences: %d\n' % len(blastp_list))

    # For HMMER output
    if tmp_filename.find('.hmmer_tbl') >= 0:
        sys.stderr.write('Read %s\n' % tmp_filename)
        f_hmmer = open_file(tmp_filename)
        for line in f_hmmer:
            if line.startswith('#'):
                continue

            tokens = line.strip().split()
            q_id = tokens[0]
            q_tokens = q_id.split('|')
            seq_id = '|'.join(q_tokens[:-1])
            tmp_frame = q_tokens[-1]
            tmp_evalue = float(tokens[4])

            if tmp_evalue > hmmsearch_Evalue_cutoff:
                continue

            # print(tokens[2], tokens[3])
            if seq_id not in hmmer_list:
                hmmer_list[seq_id] = dict()
            if tmp_frame not in hmmer_list[seq_id]:
                hmmer_list[seq_id][tmp_frame] = tmp_evalue
            elif hmmer_list[seq_id][tmp_frame] > tmp_evalue:
                hmmer_list[seq_id][tmp_frame] = tmp_evalue
        f_hmmer.close()
        sys.stderr.write('Total Sequences: %d\n' % len(hmmer_list))

f_cdna_coding = open('%s.cdna.fa' % filename_base, 'w')
f_prot_coding = open('%s.prot.fa' % filename_base, 'w')
f_prot_targets = open('%s.prot_targets' % filename_base, 'w')
f_id_list = open('%s.id_list' % filename_base, 'w')
f_cdna_orphan = open('%s.orphan_cdna.fa' % filename_base, 'w')
f_prot_orphan = open('%s.orphan_prot.fa' % filename_base, 'w')
f_noncoding = open('%s.ncdna.fa' % filename_base, 'w')

seq_idx = 1
count_seq_type = {'coding': 0, 'noncoding': 0, 'orphan': 0}
for tmp_h in cdna_seq_list.keys():
    tmp_cdna_seq = ''.join(cdna_seq_list[tmp_h])

    seq_type = 'unknown'
    best_frame = 'nn'
    best_targets = dict()

    if tmp_h not in blastp_list:
        if tmp_h not in hmmer_list:
            seq_type = 'noncoding'
        elif len(hmmer_list[tmp_h]) > 1:
            seq_type = 'noncoding'
        else:
            seq_type = 'orphan'
            best_frame = list(hmmer_list[tmp_h].keys())[0]
    else:
        if len(blastp_list[tmp_h]) == 1:
            best_frame = list(blastp_list[tmp_h].keys())[0]
            best_targets = blastp_list[tmp_h][best_frame]

            if len(best_targets) >= min_best_targets:
                seq_type = 'coding'
            else:
                seq_type = 'orphan'
        else:
            frame2count = dict()
            frame2bits = dict()
            for tmp_frame in blastp_list[tmp_h].keys():
                tmp_target_count = len(blastp_list[tmp_h][tmp_frame])
                frame2count[tmp_frame] = tmp_target_count
                frame2bits[tmp_frame] = \
                    max(blastp_list[tmp_h][tmp_frame].values())

            sorted_frame = sorted(frame2bits.keys(), key=frame2bits.get)[::-1]
            best_frame = sorted_frame[0]
            second_frame = sorted_frame[1]

            if frame2count[best_frame] > frame2count[second_frame]:
                best_targets = blastp_list[tmp_h][best_frame]
                seq_type = 'coding'
            else:
                seq_type = 'orphan'

    count_seq_type[seq_type] += 1

    seq_h = '%s.%08d' % (data_name, seq_idx)
    seq_idx += 1
    # seq_h = tmp_h

    f_id_list.write('%s\t%s\t%s\n' % (seq_h, seq_type, tmp_h))
    if seq_type == 'noncoding':
        f_noncoding.write('>t.%s\n%s\n' % (seq_h, tmp_cdna_seq))
    else:
        tmp_prot_h = '%s|%s' % (tmp_h, best_frame)
        tmp_prot_seq = ''.join(prot_seq_list[tmp_prot_h])
        if seq_type == 'coding':
            tmp_best_bits = max(blastp_list[tmp_h][best_frame].values())
            f_prot_coding.write('>p.%s\n%s\n' % (seq_h, tmp_prot_seq))
            f_cdna_coding.write('>t.%s\n%s\n' % (seq_h, tmp_cdna_seq))
            tmp_target_list = \
                sorted(best_targets.keys(), key=best_targets.get, reverse=True)
            tmp_target_str = ';'.join(["%s=%.1f" % (x, best_targets[x]) for x in tmp_target_list])
            f_prot_targets.write('p.%s\t%.1f\t%s\n' % (seq_h, tmp_best_bits, tmp_target_str))
        elif seq_type == 'orphan':
            f_prot_orphan.write('>p.%s\n%s\n' % (seq_h, tmp_prot_seq))
            f_cdna_orphan.write('>t.%s\n%s\n' % (seq_h, tmp_cdna_seq))
        else:
            sys.stderr.write('Error: %s\n' % seq_h)
