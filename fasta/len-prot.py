#!/usr/bin/env python
import os
import sys
import gzip

len_list = []
locus_list = []

filename = sys.argv[1]
f = open(filename,'r')
if( filename.endswith('.gz') ):
    f = gzip.open(filename,'rb')

h = ''
len_dist = dict()
for line in f:
    if( line.strip() == '' ):
        continue

    if( line.startswith('>') ):
        h = line.strip()
        len_dist[h] = 0
    else:
        len_dist[h] += len(line.strip())
f.close()

len_list = len_dist.values()
locus_list = len_dist.keys()

print "Count: ",len(len_list),len(list(set(locus_list)))
print "Mean: ",sum(len_list)/len(len_list)
print "Median: ",sorted(len_list)[ int(len(len_list)*0.5) ]
count_lt100 = len([x for x in len_list if x > 100])
print ">100aa: %d (%.3f)"%(count_lt100, count_lt100*100.0/len(len_dist))
print ">1000aa: ",len([x for x in len_list if x > 1000])
print ">3000aa: ",len([x for x in len_list if x > 3000])
