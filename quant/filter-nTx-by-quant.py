#!/usr/bin/env python3
import sys
import gzip

filename_nTx = sys.argv[1]
#filename_nTx = 'TKLab201907n_PELCHtx_mms9171+Heart_NoPart_nTx.fa'
filename_quant = filename_nTx.replace('_NoPart_nTx.fa', '.salmon_quant.sf')

f_nTx = open(filename_nTx, 'r')
if filename_nTx.endswith('.gz'):
    f_nTx = gzip.open(filename_nTx, 'rt')
    filename_quant = filename_nTx.replace('_NoPart_nTx.fa.gz', '.salmon_quant.sf')

tx2quant = dict()
f_quant = open(filename_quant, 'r')
h_quant = f_quant.readline()
for line in f_quant:
    tokens = line.strip().split("\t")
    tx_id = tokens[0]
    tx_tpm = float(tokens[-2])
    tx_reads = float(tokens[-1])
    tx2quant[tx_id] = {'tpm': tx_tpm, 'reads': tx_reads}
f_quant.close()

is_print = -1
for line in f_nTx:
    if line.startswith('>'):
        tx_id = line.strip().lstrip('>')
        if tx_id not in tx2quant:
            is_print = -1
        elif tx2quant[tx_id]['reads'] < 1.0:
            is_print = -1
        else:
            is_print = 1
            print(">%s tpm=%.3f;reads=%.3f" % (tx_id, tx2quant[tx_id]['tpm'], tx2quant[tx_id]['reads']))
    elif is_print > 0:
        print(line.strip())
f_nTx.close()
