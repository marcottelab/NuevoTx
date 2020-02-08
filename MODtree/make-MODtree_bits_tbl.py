#!/usr/bin/env python3
import sys

filename_self = sys.argv[1]

tf_bits = dict()
f_self = open(filename_self, 'r')
for line in f_self:
    tokens = line.strip().split("\t")
    q_id = tokens[0]
    q_fid = q_id.split('|')[0]
    t_id = tokens[1]
    t_fid = t_id.split('|')[0]
    tmp_bits = float(tokens[-1])
    tmp_id = ';'.join(sorted([q_id, t_id]))

    if q_fid not in tf_bits:
        tf_bits[q_fid] = dict()
        tf_bits[q_fid]['self'] = {'min_id': 'NotAvail', 'min_bits': 0.0, 'max_id': 'NotAvail', 'max_bits': 0.0}
        tf_bits[q_fid]['non_self'] = {'max_id': 'NotAvail', 'max_bits': 0.0}
    
    if q_fid == t_fid:
        if tf_bits[q_fid]['self']['min_id'] == 'NotAvail':
            tf_bits[q_fid]['self']['min_id'] = tmp_id
            tf_bits[q_fid]['self']['min_bits'] = tmp_bits
        
        if tf_bits[q_fid]['self']['max_id'] == 'NotAvail':
            tf_bits[q_fid]['self']['max_id'] = tmp_id
            tf_bits[q_fid]['self']['max_bits'] = tmp_bits

        if tf_bits[q_fid]['self']['min_bits'] > tmp_bits:
            tf_bits[q_fid]['self']['min_id'] = tmp_id
            tf_bits[q_fid]['self']['min_bits'] = tmp_bits

        if tf_bits[q_fid]['self']['max_bits'] < tmp_bits:
            tf_bits[q_fid]['self']['max_id'] = tmp_id
            tf_bits[q_fid]['self']['max_bits'] = tmp_bits
    else:
        if tf_bits[q_fid]['non_self']['max_id'] == 'NotAvail':
            tf_bits[q_fid]['non_self']['max_id'] = tmp_id
            tf_bits[q_fid]['non_self']['max_bits'] = tmp_bits

        tf_bits[q_fid]['non_self']['max_id'] = tmp_id
        tf_bits[q_fid]['non_self']['max_bits'] = tmp_bits
        if tf_bits[q_fid]['non_self']['max_bits'] < tmp_bits:
            tf_bits[q_fid]['non_self']['max_id'] = tmp_id
            tf_bits[q_fid]['non_self']['max_bits'] = tmp_bits
f_self.close()

print("#MODtreeID\tSelfMaxBits\tSelfMaxIDs\tSelfMinBits\tSelfMinIDs\tNonSelfMaxBits\tNonSelfMaxIDs")
for tmp_fid in sorted(tf_bits.keys()):
    tmp_self = tf_bits[tmp_fid]['self']
    tmp_nonself = tf_bits[tmp_fid]['non_self']
    print("%s\t%.1f\t%s\t%.1f\t%s\t%.1f\t%s" % (tmp_fid, tmp_self['max_bits'], tmp_self['max_id'],\
                                          tmp_self['min_bits'], tmp_self['min_id'],
                                          tmp_nonself['max_bits'], tmp_nonself['max_id']))

