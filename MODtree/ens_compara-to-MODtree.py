#!/usr/bin/env python3
import os
import sys
import gzip

dirname_compara = sys.argv[1]
ens_version = sys.argv[2]

dirname_curr = os.path.dirname(os.path.realpath(__file__))
filename_spec_list = 'MODtree.species_list.txt'
filename_spec_list = os.path.join(dirname_curr, filename_spec_list)

sp_name2code = dict()
f_spec_list = open(filename_spec_list, 'r')
for line in f_spec_list:
    tokens = line.strip().split("\t")
    sp_code = tokens[0]
    sp_name = tokens[1]
    sp_name2code[sp_name] = sp_code
f_spec_list.close()

# from ftp://ftp.ensembl.org/pub/release-100/emf/ensembl-compara/
filename_fa = 'Compara.%s.protein_default.aa.fasta.gz' % ens_version
filename_fa = os.path.join(dirname_compara, filename_fa)
filename_nh = 'Compara.%s.protein_default.nh.emf.gz' % ens_version
filename_nh = os.path.join(dirname_compara, filename_nh)

filename_out_txt = 'MODtree_compara_ens%s.raw.txt' % (ens_version)
filename_out_fa = 'MODtree_compara_ens%s.raw.fa' % (ens_version)
filename_out_log = 'MODtree_compara_ens%s.raw.log' % (ens_version)

f_out_txt = open(filename_out_txt, 'w')
f_out_log = open(filename_out_log, 'w')

family_id = 1
prot_info = dict()
tmp_prot_list = []

sys.stderr.write('Read %s\n' % filename_nh)
f_nh = gzip.open(filename_nh, 'rt')
for line in f_nh:
    line = line.strip()
    if line == '':
        continue

    if line.startswith('SEQ'):
        tokens = line.strip().split()
        sp_name = tokens[1]
        p_id = tokens[2]
        gene_name = tokens[8]
        if gene_name == 'NULL':
            gene_name = 'NotAvail'
        if sp_name in sp_name2code:
            sp_code = sp_name2code[sp_name]
            prot_info[p_id] = {'name': gene_name,
                               'sp_name': sp_name,
                               'sp_code': sp_code}
            tmp_prot_list.append(p_id)

    elif line.startswith('DATA'):
        tmp_tree_str = next(f_nh).strip()
        for tmp_p in tmp_prot_list:
            if tmp_tree_str.find(tmp_p) >= 0:
                # MODTree Family ID
                mtf_id = 'E%sF%05d' % (ens_version, family_id)

                sp_code = prot_info[tmp_p]['sp_code']
                gene_name = prot_info[tmp_p]['name']
                # Revise troublesome gene name
                gene_name = gene_name.replace(' ', '_').replace(':', '_')
                gene_name = gene_name.replace('(', '_').replace(')', '_')
                gene_name = gene_name.replace('/', '_')
                gene_name = gene_name.replace("'", "_")
                if gene_name != prot_info[tmp_p]['name']:
                    f_out_log.write('GeneName\t%s\t%s\n' %
                                    (prot_info[tmp_p]['name'], gene_name))
                tmp_h = '%s|%s|%s|%s' % (mtf_id, sp_code, gene_name, tmp_p)
                prot_info[tmp_p]['header'] = tmp_h
                f_out_txt.write("%s\t%s\t%s\t%s\t%s\n" %
                                (tmp_h, mtf_id, tmp_p, sp_code, gene_name))
        family_id += 1

    elif line.startswith('//'):
        tmp_prot_list = []

    else:
        sys.stderr.write('Error.\n')
f_nh.close()
f_out_txt.close()
f_out_log.close()

is_print = 0
seq_list = dict()
sys.stderr.write('Read %s\n' % filename_fa)
f_fa = gzip.open(filename_fa, 'rt')
for line in f_fa:
    if line.startswith('>'):
        seq_h = line.strip().lstrip('>')
        if seq_h in prot_info:
            tmp_h = '%s' % prot_info[seq_h]['header']
            seq_list[tmp_h] = []
            is_print = 1
        else:
            is_print = 0
    elif is_print > 0:
        seq_list[tmp_h].append(line.strip())
f_fa.close()
f_out_fa = open(filename_out_fa, 'w')
for tmp_h in seq_list.keys():
    tmp_seq = ''.join(seq_list[tmp_h]).replace('-', '')
    tmp_seq = tmp_seq.replace('//', '').replace('*', '')
    f_out_fa.write('>%s\n%s\n' % (tmp_h, tmp_seq))
f_out_fa.close()
