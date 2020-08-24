#!/usr/bin/env python3
import sys

#SEQ homo_sapiens ENSP00000339726 1 248681369 248682304 -1 ENSG00000189181 OR14I1
sp_name2code = dict()
f_species = open('MODtree_ensembl.species_list.txt', 'r')
for line in f_species:
    tokens = line.strip().split("\t")
    sp_code = tokens[0]
    sp_name = tokens[1]
    sp_name2code[sp_name] = sp_code
f_species.close()

ens_version = 95

# from ftp://ftp.ensembl.org/pub/release-95/emf/ensembl-compara/
filename_fa = 'Compara.%d.protein_default.aa.fasta' % ens_version
filename_nh = 'Compara.%d.protein_default.nh.emf' % ens_version

filename_out_txt = 'MODtree_ens%d_compara.txt' % (ens_version)
filename_out_fa = 'MODtree_ens%d_compara.fa' % (ens_version)

f_out_txt = open(filename_out_txt, 'w')
family_id = 1
prot_info = dict()
tmp_prot_list = []
f_nh = open(filename_nh, 'r')
for line in f_nh:
    line = line.strip()
    if line == '':
        continue

    if line.startswith('SEQ'):
        tokens = line.strip().split()
        sp_name = tokens[1]
        p_id = tokens[2]
        gene_name = tokens[8]
        if sp_name in sp_name2code:
            sp_code = sp_name2code[sp_name]
            prot_info[p_id] = {'name': gene_name, 'sp_name': sp_name, 'sp_code': sp_code}
            tmp_prot_list.append(p_id)

    elif line.startswith('DATA'):
        tmp_tree_str = next(f_nh).strip()
        for tmp_p in tmp_prot_list:
            if tmp_tree_str.find(tmp_p) >= 0:
                # MODTree Family ID
                mtf_id = 'MTF%05d' % family_id

                sp_code = prot_info[tmp_p]['sp_code']
                gene_name = prot_info[tmp_p]['name']
                prot_info[tmp_p]['header'] = '%s_%s %s %s' % (tmp_p, sp_code, mtf_id, gene_name)
                f_out_txt.write("%s\t%s\t%s\t%s\n" % (mtf_id, tmp_p, sp_code, gene_name))
        family_id += 1

    elif line.startswith('//'):
        tmp_prot_list = []

    else:
        sys.stderr.write('Error.\n')
f_nh.close()
f_out_txt.close()

is_print = 0
seq_list = dict()
f_fa = open(filename_fa, 'r')
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
    tmp_seq = ''.join(seq_list[tmp_h]).replace('-','').replace('//','').replace('*','')
    f_out_fa.write('>%s\n%s\n' % (tmp_h, tmp_seq))
f_out_fa.close()

#SEQ scophthalmus_maximus ENSSMAP00000020411 9 21811542 21814458 1 ENSSMAG00000012520 NULL
