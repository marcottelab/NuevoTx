#!/usr/bin/env python3
import os
import sys
import gzip

from datetime import date
from MODtree import *

version_str = date.today().strftime('%Y%m')
usage_mesg = '\nUsage : %s <aa.fasta of TreeFam9>\n'%(os.path.basename(__file__))

if len(sys.argv) != 2:
    sys.stderr.write('%s\n'%usage_mesg)
    sys.exit(1)

dirname_aa_fa = sys.argv[1]
if not os.access(dirname_aa_fa, os.R_OK):
    sys.stderr.write('%s\n'%usage_mesg)
    sys.exit(1)

sp_info = get_sp_info()
HS_names = get_HS_prot2names()
names = get_prot2names()
sys.stderr.write('Species: %d, Names: %d\n'%(len(sp_info), len(names)))

tf_list = dict()
for filename_fa in os.listdir(dirname_aa_fa):
    tf_id = filename_fa.split('.')[0]
    tf_list[tf_id] = {'sp_list':[], 'prot_list':[]}
    f = open(os.path.join(dirname_aa_fa,filename_fa),'r')
    for line in f:
        if line.startswith('>'):
            tmp_prot_id = line.strip().lstrip('>')
            if tmp_prot_id in names:
                tmp_species = names[tmp_prot_id]['species']
                tmp_gene_name = names[tmp_prot_id]['name']
                if not tmp_species in sp_info:
                    continue
                new_prot_id = '%s.%s'%(sp_info[tmp_species]['tax_id'],tmp_prot_id)
                tf_list[tf_id]['sp_list'].append(sp_info[tmp_species]['sp_code'])
                tf_list[tf_id]['prot_list'].append(new_prot_id)
    f.close()

f_out = open('MODtree.treefam.%s.list'%version_str,'w')
f_out.write("#MODtreeID\tCountSpecies\tCountProt\tSpeciesList\tProtList\n")
for tmp_tf_id in sorted(tf_list.keys()):
    tmp_sp_list = sorted(list(set(tf_list[tmp_tf_id]['sp_list'])))
    tmp_prot_list = sorted(list(set(tf_list[tmp_tf_id]['prot_list'])))
    sp_count = len(tmp_sp_list)
    prot_count = len(tmp_prot_list)
    str_sp_list = ','.join(tmp_sp_list)
    str_prot_list = ','.join(tmp_prot_list)
    tmp_HS_name = 'NA'
    for tmp_prot_id in ['.'.join(x.split('.')[1:]) for x in tmp_prot_list]:
        if tmp_prot_id in HS_names:
            tmp_HS_name = HS_names[tmp_prot_id]
    
    if sp_count < 2 or prot_count < 2:
        continue

    f_out.write( "%s|%s\t%d\t%d\t%s\t%s\n"%(tmp_tf_id, tmp_HS_name, sp_count, \
            prot_count, str_sp_list, str_prot_list) )
f_out.close()
