# Common library for MODtree
# Author: Taejoon Kwon (tkwon@unist.ac.kr)

import os
import gzip

filename_sp_list = 'MODtree.species_list.txt'

# TreeFam version 9 --> EnsEMBL version 69
filename_names = 'ens69.prot2name.gz'

dirname_curr = os.path.dirname(os.path.realpath(__file__))


def get_tax2sp():
    tax2sp = dict()
    f_list = open(os.path.join(dirname_curr, filename_sp_list), 'r')
    for line in f_list:
        tokens = line.strip().split("\t")
        sp_code = tokens[0]
        tax_id = tokens[2]
        tax2sp[tax_id] = sp_code
    f_list.close()
    return tax2sp


def get_sp_info():
    rv = dict()
    f_list = open(os.path.join(dirname_curr, filename_sp_list), 'r')
    for line in f_list:
        tokens = line.strip().split("\t")
        sp_code = tokens[0]
        sp_name = tokens[1]
        tax_id = tokens[2]
        rv[sp_name] = {'sp_code': sp_code, 'tax_id': tax_id}
    f_list.close()
    return rv


def get_HS_prot2names():
    HS_names = dict()
    f_names = gzip.open(os.path.join(dirname_curr, filename_names), 'rt')
    for line in f_names:
        tokens = line.strip().split()
        if tokens[0] == 'Homo_sapiens':
            HS_names[tokens[1]] = tokens[2]
    f_names.close()
    return HS_names


def get_prot2names():
    prot_names = dict()
    f_names = gzip.open(os.path.join(dirname_curr, filename_names), 'rt')
    for line in f_names:
        tokens = line.strip().split()
        prot_names[tokens[1]] = {'species': tokens[0], 'name': tokens[2]}
    f_names.close()
    return prot_names
