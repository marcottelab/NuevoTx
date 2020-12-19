#!/usr/bin/env python3
import sys
import gzip

# 'ENCODE_HUMANtx_HCT116+ENCFF000DKT.spades.nTx.fa.gz'
filename_nTx = sys.argv[1]
db_name = 'MODtree_ENOG50'

sp_code = 'HYNYA'
sample_name = '_'.join(filename_nTx.split('.')[0].split('_')[2:4])
filename_base = filename_nTx.replace('.nTx.fa.gz', '')

filename_quant = '%s.nTx.kallisto_quant.tsv.gz' % filename_base
filename_modtree = '%s.nTx.transeq6.%s.dmnd_bp_out.gz' % (filename_base, db_name)
filename_prot6 = '%s.nTx.transeq6.fa.gz' % filename_base

# best_bits = dict()
# f_mt = gzip.open('../MODtree_ENOG50.uniprot+gencode.self.dmnd_top2.gz', 'rt')
# for line in f_mt:
#    tokens = line.strip().split("\t")
#    best_bits[tokens[0]] = float(tokens[1])
# f_mt.close()

nTx_list = dict()
f_nTx = gzip.open(filename_nTx, 'rt')
for line in f_nTx:
    if line.startswith('>'):
        tmp_h = line.strip().lstrip('>').replace('/', '_').split()[0]
        nTx_list[tmp_h] = []
    else:
        nTx_list[tmp_h].append(line.strip())
f_nTx.close()

prot6_list = dict()
f_prot6 = gzip.open(filename_prot6, 'rt')
for line in f_prot6:
    if line.startswith('>'):
        tmp_h = line.strip().lstrip('>').replace('/', '_').split()[0]
        prot6_list[tmp_h] = ''
    else:
        prot6_list[tmp_h] += line.strip()
f_prot6.close()

quant_list = dict()
f_kallisto = gzip.open(filename_quant, 'rt')
f_kallisto.readline()
for line in f_kallisto:
    tokens = line.strip().split("\t")
    q_id = tokens[0].replace('/', '_')
    tmp_quant = float(tokens[-1])
    quant_list[q_id] = tmp_quant
f_kallisto.close()

modtree_list = dict()
f_modtree = gzip.open(filename_modtree, 'rt')
for line in f_modtree:
    tokens = line.strip().split("\t")
    q_id = tokens[0].replace('/', '_')
    t_id = tokens[1]
    q_start = int(tokens[6])
    q_end = int(tokens[7])
    t_start = int(tokens[8])
    t_end = int(tokens[9])
    tmp_bits = float(tokens[-1])
    if q_id not in modtree_list:
        modtree_list[q_id] = {'t_id': t_id,
                              'bits': tmp_bits,
                              'qstart': q_start,
                              'qend': q_end,
                              'tstart': t_start,
                              'tend': t_end}
    elif tmp_bits > modtree_list[q_id]['bits']:
        modtree_list[q_id] = {'t_id': t_id,
                              'bits': tmp_bits,
                              'qstart': q_start,
                              'qend': q_end,
                              'tstart': t_start,
                              'tend': t_end}
f_modtree.close()

t_best = dict()
#f_out = open('%s.QM_summary' % filename_base, 'w')
for p_id in sorted(modtree_list.keys()):
    tx_id = '_'.join(p_id.split('_')[:-1])
    tmp_modtree = modtree_list[p_id]
    tmp_quant = quant_list[tx_id]
    tmp_qstart = tmp_modtree['qstart']
    tmp_qend = tmp_modtree['qend']
    tmp_tstart = tmp_modtree['tstart']
    tmp_tend = tmp_modtree['tend']
    tmp_bits = tmp_modtree['bits']
    tmp_tid = tmp_modtree['t_id']
    tmp_stop_count = prot6_list[p_id][tmp_qstart:tmp_qend].count('*')
    # tmp_tbest = best_bits[tmp_tid]

    if tmp_quant == 0.0:
        continue

    # tmp_line = "%s\t%.1f\t%.1f\t%d\t%d\t%d\t%d\t%d\t%.1f\t%s" % \
    tmp_line = "%s\t%.1f\t%.1f\t%d\t%d\t%d\t%d\t%d\t%s" % \
               (p_id, tmp_quant, tmp_bits, tmp_qstart, tmp_qend,
                tmp_tstart, tmp_tend, tmp_stop_count, tmp_tid)
    #f_out.write('%s\n' % tmp_line)

    if tmp_tid not in t_best:
        t_best[tmp_tid] = {'line': tmp_line,
                           'bits': tmp_bits,
                           'p_id': p_id,
                           'tx_id': tx_id,
                           'modtree': tmp_modtree}
    elif t_best[tmp_tid]['bits'] < tmp_bits:
        t_best[tmp_tid] = {'line': tmp_line,
                           'bits': tmp_bits,
                           'p_id': p_id,
                           'tx_id': tx_id,
                           'modtree': tmp_modtree}
#f_out.close()
#

def revcomp(tmp_seq):
    rc = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N', 'X': 'X', '*': '*'}
    return ''.join([rc[x] for x in tmp_seq[::-1]])


tmp_idx = 1
f_best = open('%s.QM_best' % filename_base, 'w')
f_best.write('#SeqID\tTPM\tBits\tQstart\tQend\tTstart\tTend\tStopCount\tTid\n')
f_best_tx = open('%s.QM_best_tx.fa' % filename_base, 'w')
f_best_pep = open('%s.QM_best_pep.fa' % filename_base, 'w')
for t_id, tmp in t_best.items():
    tmp_modtree = t_best[t_id]['modtree']

    tmp_qstart = tmp_modtree['qstart']
    tmp_qend = tmp_modtree['qend']
    tmp_tstart = tmp_modtree['tstart']
    tmp_tend = tmp_modtree['tend']
    tmp_bits = tmp_modtree['bits']
    tmp_tid = tmp_modtree['t_id']
    tmp_stop_count = prot6_list[p_id][tmp_qstart:tmp_qend].count('*')

    tmp_nseq = ''.join(nTx_list[tmp['tx_id']])
    tmp_pseq = prot6_list[tmp['p_id']][tmp_qstart:tmp_qend]

    tmp_t_tokens = tmp_tid.split('|')
    tmp_name = tmp_t_tokens[0]

    tmp_h_id = '%s.%s.%06d|%s' % (sp_code, sample_name, tmp_idx, tmp_name)
    tmp_idx += 1
    tmp_h = '%s bits=%.1f, fid=%s, plen=%d-%d' % \
            (tmp_h_id, tmp_bits, tmp_t_tokens[-1], tmp_qstart, tmp_qend)

    tmp_frame = int(tmp['p_id'].split('_')[-1])
    if tmp_frame in [1, 2, 3]:
        # tmp_nstart = tmp_qstart*3 + tmp_frame - 1
        tmp_nstart = tmp_qstart*3 - 1
        tmp_nend = tmp_nstart + (tmp_qend - tmp_qstart) * 3
        new_nstart = max(0, tmp_nstart-15)
        new_nend = min(len(tmp_nseq), tmp_nend+16)
        tmp_nseq = tmp_nseq[new_nstart: new_nend]
        #sys.stderr.write('%d - %d : %s\n' % (tmp_nstart, tmp_nend, tmp_h))

    elif tmp_frame in [4, 5, 6]:
        tmp_nstart = tmp_qstart*3 - 1
        tmp_nend = tmp_nstart + (tmp_qend - tmp_qstart) * 3
        #sys.stderr.write('%d - %d : %s\n' % (tmp_nstart, tmp_nend, tmp_h))
        tmp_nseq = revcomp(tmp_nseq)
        new_nstart = max(0, tmp_nstart-15)
        new_nend = min(len(tmp_nseq), tmp_nend+16)
        tmp_nseq = tmp_nseq[new_nstart: new_nend]

    f_best_tx.write('>t.%s\n%s\n' % (tmp_h, tmp_nseq))
    f_best_pep.write('>p.%s %d\n%s\n' % (tmp_h, tmp_frame, tmp_pseq))

    f_best.write('%s\t%s\n' % (tmp_h_id, t_best[t_id]['line']))
f_best.close()
