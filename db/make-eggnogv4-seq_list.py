#!/usr/bin/env python
import os
import sys
import gzip

################################################################################
## Make summary 'seq_list' summary file.
################################################################################

## EggNOGv4 files should be downloaded from 
## http://eggnog.embl.de/version_4.0.beta/downloads.v4.html

## Directory containing all members information, retrievied from
## http://eggnog.embl.de/version_4.0.beta/data/downloads/members/all.members.tar.gz
dirname_members = 'members'

## http://eggnog.embl.de/version_4.0.beta/data/downloads/eggnogv4.species.txt
filename_species = 'eggnogv4.species.txt'

## A file made by make-eggnogv4-core_fa.py, containing only 'core' members.
filename_seq ="eggnogv4.proteins.core.fa.gz"

filename_out = 'eggnogv4.NOG.seq_list'
core_list = dict()
f_species = open(filename_species,'r')
for line in f_species:
    if( line.startswith('#') ):
        continue
    tokens = line.strip().split("\t")
    tmp_genus = tokens[0].split()[0]
    tmp_tax_id = tokens[1]
    tmp_type = tokens[2]
    if( tmp_type == 'core' ):
        core_list[tmp_tax_id] = tmp_genus
f_species.close()

tmp_h = ''
seq_len = dict()
sys.stderr.write('Read %s\n'%filename_seq)
f = gzip.open(filename_seq,'rb')
for line in f:
    if( line.startswith('>') ):
        tmp_h = line.strip().lstrip('>')
        tmp_tax_id = tmp_h.split('.')[0]
        if( core_list.has_key(tmp_tax_id) ):
            seq_len[tmp_h] = 0
        else:
            tmp_h = ''
    elif( tmp_h != '' ):
        seq_len[tmp_h] += len(line.strip())
f.close()
sys.stderr.write('Done\n')

members = dict()
for filename in os.listdir(dirname_members):
    if( filename.find('members.txt') < 0 ):
        continue
    filename_members = os.path.join(dirname_members, filename)
    sys.stderr.write('Read %s\n'%filename_members)
    f = gzip.open(filename_members,'rb')
    for line in f:
        if( line.startswith('#') ):
            continue
        tokens = line.strip().split('\t')
        tmp_grp = tokens[0]
        if( not members.has_key(tmp_grp) ):
            members[tmp_grp] = []
        tmp_id = tokens[1]
        tmp_tax_id = tmp_id.split('.')[0]
        if( core_list.has_key(tmp_tax_id) ):
            members[tmp_grp].append( tokens[1] )
    f.close()

f_out = open(filename_out,'w')
f_out.write('#NOG_ID\tCountMembers\tLongestID\tQ50_ID\tLongestLen\tQ25_len\tQ50_len\tQ75_len\n')
for tmp_grp in sorted(members.keys()):
    if( len(members[tmp_grp]) == 0 ):
        continue
    seq_id_list = sorted(members[tmp_grp], key=seq_len.get)
    max_seq_len = seq_len[seq_id_list[-1]]
    max_seq_id = ';'.join([x for x in members[tmp_grp] if seq_len[x] == max_seq_len])
    q50_seq_len = seq_len[ seq_id_list[int(len(seq_id_list)*0.5)] ]
    q50_seq_id = ';'.join([x for x in members[tmp_grp] if seq_len[x] == q50_seq_len])
    q25_seq_len = seq_len[ seq_id_list[int(len(seq_id_list)*0.25)] ]
    q75_seq_len = seq_len[ seq_id_list[int(len(seq_id_list)*0.75)] ]

    f_out.write('%s\t%d\t%s\t%s\t%d\t%d\t%d\t%d\n'%(tmp_grp,len(members[tmp_grp]),max_seq_id,q50_seq_id,max_seq_len,q25_seq_len,q50_seq_len,q75_seq_len))
f_out.close()
