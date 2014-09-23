#!/usr/bin/env python
import os
import sys
import gzip
import random

################################################################################
## Make 'representative' sequences from TreeFam9 based on query species list.
## 1. If a family has only one gene from defined query species, use it.
## 2. If a famliy has more than one gene, select one with 'median length'.
##   If there is more than one sequences with same 'median length', 
##   select any of them randomly.
################################################################################

## Prerequisites. 
## These files should be downloaded from http://www.treefam.org/download

## http://www.treefam.org/static/download/treefam9.fa.tar.gz
filename_tf9 = 'treefam9.fa.gz'

## http://www.treefam.org/static/download/treefam9_species.tar
dirname_species = 'treefam9_species'

## Species list to make representative sequence database
## Matched to filenames under 'treefam9_species' directory
## My 'core species' list is available under github
filename_species = 'treefam9_species.core'

core_list = dict()
f_sp = open(filename_species,'r')
for line in f_sp:
    tokens = line.strip().split()
    common_name = tokens[0]
    sp_name = tokens[1]

    seq_h = ''
    sys.stderr.write('Read %s file ... '%sp_name)
    f_fa = open(os.path.join(dirname_species,'%s.fa'%sp_name),'r')
    for line in f_fa:
        if( line.startswith('>') ):
            seq_h = line.strip().lstrip('>')
            core_list[seq_h] = common_name
    f_fa.close()
    sys.stderr.write('Done\n')
f_sp.close()

tf_id = ''
tf2members = dict()
f_tf9 = gzip.open(filename_tf9,'rb')
for line in f_tf9:
    if( line.startswith('TF') and len(line) < 16 ):
        tf_id = line.strip()
        tf2members[ tf_id ] = dict()
    elif( line.startswith('>') ):
        tmp_h = line.strip().lstrip('>')
        if( core_list.has_key(tmp_h) ):
            tf2members[tf_id][tmp_h] = {'h': '%s|%s|%s'%(tf_id,tmp_h,core_list[tmp_h]), 'seq_list':[]}
        else:
            tmp_h = '' 
    elif( tmp_h != '' ):
        tf2members[tf_id][tmp_h]['seq_list'].append(line.strip())
f_tf9.close()

## All sequences from 'species list'
f_all = open('treefam9_all.fa','w')
## Gene family having more than one gene (based on species list)
f_multi = open('treefam9_multi.fa','w')
## One protein/family file based with median length of each family
f_rep = open('treefam9_rep.fa','w')
f_log = open('treefam9_all.log','w')
for tf_id in tf2members.keys():
    count_members = len(tf2members[tf_id])
    species_list = sorted(list(set([core_list[x] for x in tf2members[tf_id]])))
    count_species = len(species_list)
    if( count_species == 0 ):
        continue
    
    elif( count_species == 1 ):
        for tmp_h in tf2members[tf_id].keys():
            tmp_header = tf2members[tf_id][tmp_h]['h']
            tmp_seq = ''.join(tf2members[tf_id][tmp_h]['seq_list'])
            f_all.write('>%s\n%s\n'%(tmp_header,tmp_seq))
            f_rep.write('>%s\n%s\n'%(tmp_header,tmp_seq))
    else:
        seqlen = dict()
        for tmp_h in tf2members[tf_id].keys():
            tmp_header = tf2members[tf_id][tmp_h]['h']
            tmp_seq = ''.join(tf2members[tf_id][tmp_h]['seq_list'])
            f_multi.write('>%s\n%s\n'%(tmp_header,tmp_seq))
            f_all.write('>%s\n%s\n'%(tmp_header,tmp_seq))
            seqlen[tmp_h] = len(tmp_seq)
        
        median_len = sorted(seqlen.values())[ int(len(seqlen)*0.5) ]
        median_len_seq = [x for x in seqlen.keys() if seqlen[x] == median_len]
        random.shuffle(median_len_seq)
        median_h = median_len_seq[0]
        tmp_header = tf2members[tf_id][median_h]['h']
        tmp_seq = ''.join(tf2members[tf_id][median_h]['seq_list'])
        f_rep.write('>%s\n%s\n'%(tmp_header,tmp_seq))

    f_log.write('%s\t%d\t%d\t%s\n'%(tf_id,count_members,count_species,','.join(species_list)))
f_log.close()
f_all.close()
f_rep.close()
f_multi.close()
