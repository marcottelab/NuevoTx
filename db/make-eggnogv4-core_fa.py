#!/usr/bin/env python3
import gzip

###############################################################################
# Make FASTA file only with core members.
###############################################################################

# EggNOGv4 files should be downloaded from
# http://eggnog.embl.de/version_4.0.beta/downloads.v4.html

# http://eggnog.embl.de/version_4.0.beta/data/downloads/eggnogv4.species.txt
filename_species = 'eggnogv4.species.txt'

# http://eggnog.embl.de/version_4.0.beta/data/downloads/eggnogv4.proteins.all.fa.gz
filename_seq = "eggnogv4.proteins.all.fa.gz"

filename_out = 'eggnogv4.proteins.core.fa'
core_list = dict()
f_species = open(filename_species, 'r')
for line in f_species:
    if line.startswith('#'):
        continue
    tokens = line.strip().split("\t")
    tmp_genus = tokens[0].split()[0]
    tmp_tax_id = tokens[1]
    tmp_type = tokens[2]
    if tmp_type == 'core':
        core_list[tmp_tax_id] = tmp_genus
f_species.close()

tmp_h = ''
seq_len = dict()
f_in = gzip.open(filename_seq, 'rt')
f_out = open(filename_out, 'w')
for line in f_in:
    if line.startswith('>'):
        tmp_h = line.strip().lstrip('>')
        tmp_tax_id = tmp_h.split('.')[0]
        if tmp_tax_id in core_list:
            f_out.write('>%s\n' % tmp_h)
        else:
            tmp_h = ''
    elif tmp_h != '':
        f_out.write('%s\n' % line.strip())
f_in.close()
f_out.close()
