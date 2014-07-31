#!/usr/bin/env python
import os
import sys
import gzip

filename_fq = sys.argv[1]

count_total = 0
count_nocall = 0
count_low_complex = 0

filename_base = filename_fq.split('.')[0]
sys.stderr.write('%s -> %s_called.fastq\n'%(filename_fq,filename_base))

f_fq = open(filename_fq,'r')
if( filename_fq.endswith('.gz') ):
    f_fq = gzip.open(filename_fq,'rb')
    filename_base = filename_base.replace('.gz','')

nfreq_called = dict()
nfreq_raw = dict()
read_len = 0

f_out = open('%s_called.fastq'%filename_base,'w')
for line in f_fq:
    if( line.startswith('@') ):
        nseq = f_fq.next().strip()
        f_fq.next()
        qseq = f_fq.next().strip()
        if( read_len == 0 ):
            read_len = len(nseq)
            for tmp_i in range(0,read_len):
                nfreq_raw[tmp_i] = {'A':0,'T':0,'G':0,'C':0,'N':0}
                nfreq_called[tmp_i] = {'A':0,'T':0,'G':0,'C':0,'N':0}
        
        count_total += 1

        if( nseq.find('N') >= 0 or nseq.find('.') >= 0 ):
            count_nocall += 1
            for tmp_i in range(0,read_len):
                tmp_nseq = 'N'
                nfreq_raw[tmp_i][ tmp_nseq ] += 1
        elif( nseq.find('A') < 0 or nseq.find('T') < 0 or nseq.find('G') < 0 or nseq.find('C') < 0 ):
            count_low_complex += 1
            for tmp_i in range(0,read_len):
                nfreq_raw[tmp_i][ nseq[tmp_i] ] += 1
        else:
            f_out.write("%s\n%s\n+\n%s\n"%(line.strip(),nseq,qseq))
            for tmp_i in range(0,read_len):
                nfreq_raw[tmp_i][ nseq[tmp_i] ] += 1
                nfreq_called[tmp_i][ nseq[tmp_i] ] += 1
f_fq.close()
f_out.close()

f_raw = open('%s.pos_call'%filename_base,'w')
f_called = open('%s.called.pos_call'%filename_base,'w')
f_raw.write('Pos\tA\tT\tG\tC\tN\n')
f_called.write('Pos\tA\tT\tG\tC\n')
for tmp_pos in range(0,read_len):
    tmp_raw = nfreq_raw[tmp_pos]
    tmp_called = nfreq_called[tmp_pos]
    f_raw.write('%d\t%d\t%d\t%d\t%d\t%d\n'%(tmp_pos,tmp_raw['A'],tmp_raw['T'],tmp_raw['G'],tmp_raw['C'],tmp_raw['N']))
    f_called.write('%d\t%d\t%d\t%d\t%d\n'%(tmp_pos,tmp_called['A'],tmp_called['T'],tmp_called['G'],tmp_called['C']))
f_raw.close()
f_called.close()

f_log = open('%s.log'%filename_base,'a')
f_log.write("Command: filter-nocall.py %s\n"%filename_fq)
f_log.write("Total reads: %d\n"%count_total)
f_log.write("Reads with nocall: %d\n"%count_nocall)
f_log.write("Reads with low complexity (type of N < 4): %d\n"%count_low_complex)
f_log.write("Total called: %d\n"%(count_total - count_nocall - count_low_complex))
f_log.write("\n")
f_log.close()
