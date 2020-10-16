#!/usr/bin/env python3
import sys
import os

dirname_spades = sys.argv[1]
dirname_base = os.path.basename(dirname_spades).split('.')[0]
sys.stderr.write('%s\n' % dirname_base)

if not os.access(dirname_spades, os.R_OK):
    sys.stderr.write('%s is not available. Exit.\n' % dirname_spades)
    sys.exit(1)

filename_source_fa = os.path.join(dirname_spades, 'transcripts.fasta')
filename_target_fa = '%s.spades.nTx.fa' % (dirname_base)

if not os.access(filename_source_fa, os.R_OK):
    sys.stderr.write('%s is not available. Exit.\n' % filename_source_fa)
    sys.exit(1)

f_fa = open(filename_source_fa, 'r')
f_out = open(filename_target_fa, 'w')
sys.stderr.write('Write %s\n' % filename_target_fa)
for line in f_fa:
    if line.startswith('>'):
        tmp_h = line.strip().lstrip('>')
        new_h = '%s_%s' % (dirname_base, tmp_h)
        f_out.write('>%s\n' % new_h)
    else:
        f_out.write("%s\n" % line.strip())
f_out.close()
