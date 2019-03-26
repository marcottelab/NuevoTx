#!/usr/bin/env python
import sys
import gzip

len_list = []
locus_list = []

filename = sys.argv[1]
f = open(filename, 'r')
if filename.endswith('.gz'):
    f = gzip.open(filename, 'rt')

h = ''
len_dist = dict()
for line in f:
    if line.startswith('>'):
        h = line.strip()
        len_dist[h] = 0
    else:
        len_dist[h] += len(line.strip())
f.close()

len_list = len_dist.values()
locus_list = len_dist.keys()

print("Count: %d %d\n" % (len(len_list), len(list(set(locus_list)))))
print("Mean: %d\n" % sum(len_list)/len(len_list))
print("Median: %d\n" % sorted(len_list)[int(len(len_list)*0.5)])
print(">400bp: %d\n" % len([x for x in len_list if x > 400]))
print(">1000bp: %d\n" % len([x for x in len_list if x > 1000]))
print(">10kbp: %d\n" % len([x for x in len_list if x > 10000]))
