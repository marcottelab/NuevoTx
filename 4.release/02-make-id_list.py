#!/usr/bin/env python3
import gzip
import sys

#filename_fa = 'Karsenia_koreana.prot.select.2021_07.fa'
#filename_bp = 'Karsenia_koreana.prot.select.2021_07.MODtree_ens100_2021_05.dmnd_bp_tbl6.gz'
#sp_code = 'KARKO'

filename_fa = sys.argv[1]
filename_bp = sys.argv[2]
sp_code = sys.argv[3]

q_best = dict()
t_best = dict()
gencode_best = dict()
final_list = dict()

seq_list = dict()
f_fa = open(filename_fa, 'r')
if filename_fa.endswith('.gz'):
    f_fa = gzip.open(filename_fa, 'rt')
for line in f_fa:
    if line.startswith('>'):
        tmp_h = line.strip().lstrip('>')
        tmp_h_id = tmp_h.split()[0]
        seq_list[tmp_h_id] = {'h': tmp_h, 'seq': ''}
    else:
        seq_list[tmp_h_id]['seq'] += line.strip()
f_fa.close()

f_bp = open(filename_bp, 'rt')
if filename_bp.endswith('.gz'):
    f_bp = gzip.open(filename_bp, 'rt')
for line in f_bp:
    tokens = line.strip().split("\t")
    q_id = tokens[0]
    t_id = tokens[1]
    tmp_bits = float(tokens[-1])

    if q_id not in q_best:
        q_best[q_id] = {'t_id': t_id, 'bits': tmp_bits}
    elif q_best[q_id]['bits'] < tmp_bits:
        q_best[q_id] = {'t_id': t_id, 'bits': tmp_bits}
    
    if t_id not in t_best:
        t_best[t_id] = {'q_id': q_id, 'bits': tmp_bits}
    elif t_best[t_id]['bits'] < tmp_bits:
        t_best[t_id] = {'q_id': q_id, 'bits': tmp_bits}
    
    if t_id.find('-GENCODE') >= 0:
        if t_id not in gencode_best:
            gencode_best[t_id] = {'q_id': q_id, 'bits': tmp_bits}
        elif gencode_best[t_id]['bits'] < tmp_bits:
            gencode_best[t_id] = {'q_id': q_id, 'bits': tmp_bits}
f_bp.close()


def is_good_name(tmp_name):
    if tmp_name.upper() == 'NOTAVAIL':
        return False
    if tmp_name.find('SI_DKEY') >= 0:
        return False
    if sum(c.isdigit() for c in tmp_name) > 4:
        if tmp_name.startswith('ZNF') or tmp_name.startswith('SLC'):
            return True
        else:
            #print("Wrong name", tmp_name)
            return False
    return True


for tmp_q_id, tmp_q in q_best.items():
    tmp_t = tmp_q['t_id'] 
    family_id = tmp_t.split('|')[0]
    family_class = tmp_t.split('|')[-1]

    gene_name = tmp_t.split('|')[2].upper()
    if not is_good_name(gene_name):
        gene_name = 'NotAvail'

    if family_class in ['IG', 'OR']:
        final_list[tmp_q_id] = '%s|%s|%s|%s|%s' % (family_id, sp_code, gene_name, tmp_q_id, family_class)
    elif family_class.startswith('single_'):
        final_list[tmp_q_id] = '%s|%s|%s|%s|%s' % (family_id, sp_code, gene_name, tmp_q_id, family_class)
    elif family_class == 'noname':
        final_list[tmp_q_id] = '%s|%s|%s|%s|%s' % (family_id, sp_code, gene_name, tmp_q_id, family_class)

sys.stderr.write('Prefilter: %d \n' % len(final_list))

name_best = dict()
name_list = dict()
for tmp_t_id, tmp_t in gencode_best.items():
    tmp_name = tmp_t_id.split('|')[2].upper()
    tmp_q_id = tmp_t['q_id']
    tmp_bits = tmp_t['bits']

    if tmp_q_id in final_list:
        continue

    if is_good_name(tmp_name):
        if tmp_name not in name_best:
            name_list[tmp_name] = []
            name_best[tmp_name] = {'q_id': tmp_q_id, 't_id': tmp_t_id, 'bits': tmp_bits}
        
        if name_best[tmp_name]['bits'] < tmp_bits:
            name_best[tmp_name] = {'q_id': tmp_q_id, 't_id': tmp_t_id, 'bits': tmp_bits}

for tmp_name in name_best.keys():
    tmp_q_id = name_best[tmp_name]['q_id']
    tmp_t_id = name_best[tmp_name]['t_id']
    family_id = tmp_t_id.split('|')[0]
    family_class = tmp_t_id.split('|')[-1]
    final_list[tmp_q_id] = '%s|%s|%s|%s|%s' % (family_id, sp_code, tmp_name, tmp_q_id, family_class)

sys.stderr.write('Prefilter+Named: %d \n' % len(final_list))

final_family_list = [x.split('|')[0] for x in final_list.values()]
for tmp_q_id, tmp_q in q_best.items():
    tmp_t_id = tmp_q['t_id']
    family_id = tmp_q['t_id'].split('|')[0]
    family_class = tmp_q['t_id'].split('|')[-1]

    if family_id not in final_family_list:
        tmp_name = tmp_t_id.split('|')[2].upper()
        if not is_good_name(tmp_name):
            tmp_name = 'NotAvail'
        final_list[tmp_q_id] = '%s|%s|%s|%s|%s' % (family_id, sp_code, tmp_name, tmp_q_id, family_class)

sys.stderr.write('Prefilter+Named+Draft: %d \n' % len(final_list))

last_idx = 0
print("#tx_ID\tprot_ID\tfamily_ID\tfamily_class\tgene_name\torig_ID\tExtra")
for tmp_old_h, tmp_new_h in final_list.items():
    last_idx += 1
    tx_id = 'AB%sT%07d' % (sp_code, last_idx)
    prot_id = 'AB%sP%07d' % (sp_code, last_idx)
    new_tokens = tmp_new_h.split('|')
    family_id = new_tokens[0]
    gene_name = new_tokens[2]
    old_id = new_tokens[3]
    family_class = new_tokens[4]
    tmp_extra = seq_list[tmp_old_h]['h'].replace(tmp_old_h, '')

    print("%s\t%s\t%s\t%s\t%s\t%s\t%s" % (tx_id, prot_id, family_id, family_class, gene_name, tmp_old_h, tmp_extra))
    #tmp_seq = seq_list[tmp_old_h]['seq']
    #print(">%s %s\n%s" % (tmp_new_h, tmp_extra, tmp_seq))
