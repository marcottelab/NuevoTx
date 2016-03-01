#!/usr/bin/python
import os
import sys
import gzip
import re

filename_transl_tbl = 'tbl01.standard'

__dir__ = os.path.dirname(os.path.realpath(__file__))
transl_tbl_list = [x for x in os.listdir(__dir__) if x.startswith('tbl')]
usage = '\n  Usage: %s <fasta file> (optional <transl_tbl>)\n\n'%(os.path.basename(__file__))
usage += '    transl_tbl: %s\n'%(', '.join(transl_tbl_list))
usage += '    default transl_tbl is %s\n\n'%filename_transl_tbl

min_plen = 6
if( len(sys.argv) == 1 ):
    sys.stderr.write('%s\n'%usage)
    sys.exit(1)

filename_fa = sys.argv[1]
filename_base = re.sub(r'.fa[sta]*$','',filename_fa)
if( not os.access(filename_fa,os.R_OK) ):
    sys.stderr.write('%s is not available. Exit.\n'%filename_base)
    sys.exit(1)

if( len(sys.argv) > 2 ):
    filename_transl_tbl = sys.argv[2]
    if( not filename_transl_tbl in transl_tbl_list ):
        sys.stderr.write('%s is not available. Exit.\n'%filename_transl_tbl)
        sys.exit(1)

sys.stderr.write('Input: %s\n'%filename_fa)
sys.stderr.write('Transl_TBL: %s\n'%filename_transl_tbl)

seq_list = dict()
seq_frame = dict()

seq_h = ''
f_fa = open(filename_fa,'r')
if( filename_fa.endswith('.gz') ):
    f_fa = gzip.open(filename_fa,'rb')
    filename_base = re.sub(r'.fa[sta].gz*$','',filename_fa)

for line in f_fa:
    if( line.startswith('>') ):
        seq_h = line.strip().lstrip('>')
        seq_list[seq_h] = []
    else:
        seq_list[seq_h].append(line.strip().upper())
f_fa.close()

f_transl_tbl = open(os.path.join(__dir__,filename_transl_tbl),'r')
header = f_transl_tbl.readline()
AAs    = f_transl_tbl.readline().strip()
Starts = f_transl_tbl.readline().strip()
Base1  = f_transl_tbl.readline().strip()
Base2  = f_transl_tbl.readline().strip()
Base3  = f_transl_tbl.readline().strip()
f_transl_tbl.close()

rc = {'A':'T','T':'A','G':'C','C':'G','N':'N','M':'M','R':'R','S':'S','Y':'Y','D':'D','W':'W','K':'K','V':'V','B':'B'}
trans_tbl = dict()

for i in range(0,len(AAs)):
    trans_tbl['%s%s%s'%(Base1[i],Base2[i],Base3[i])] = AAs[i]

def translate(tmp_nseq):
    rv = []
    for i in range(0,len(tmp_nseq)-2,3):
        tmp_codon = tmp_nseq[i:i+3]
        if( not trans_tbl.has_key(tmp_codon) ):
            rv.append('*')
        else:
            rv.append( trans_tbl[tmp_codon] )
    return ''.join(rv)

def revcomp(tmp_nseq):
    return ''.join([rc[x] for x in tmp_nseq.upper()[::-1]])

f_pfa = open('%s_prot6.fa'%filename_fa.replace('.fa',''),'w')

for tmp_h in sorted(seq_list.keys()):
    tmp_nseq = ''.join(seq_list[tmp_h])
    tmp_nseq = tmp_nseq.replace('H','A')
    tmp_rc_nseq = revcomp(tmp_nseq)

    tmp_p6 = dict()
    tmp_p6['f0'] = translate(tmp_nseq[0:])
    tmp_p6['f1'] = translate(tmp_nseq[1:])
    tmp_p6['f2'] = translate(tmp_nseq[2:])

    tmp_p6['r0'] = translate(tmp_rc_nseq[0:])
    tmp_p6['r1'] = translate(tmp_rc_nseq[1:])
    tmp_p6['r2'] = translate(tmp_rc_nseq[2:])

    for tmp_pf in tmp_p6.keys():
        tmp_p = tmp_p6[tmp_pf]
        longest_pep = ''
        for tmp_pep in tmp_p.split('*'):
            if( len(tmp_pep) > len(longest_pep) ):
                longest_pep = tmp_pep
    
        if( len(longest_pep) < min_plen ):
            continue
         
        f_pfa.write('>%s|%s\n%s\n'%(tmp_h,tmp_pf,longest_pep))
f_pfa.close()
