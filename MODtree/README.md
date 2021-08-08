# MODtree: the reference database for NuevoTx

## Prepare GENCODE human/mouse sequences

1. Doownload pc_translate files from GENCODE website.

2. Convert the header of GENCODE FASTA files compatible to MODtree.
  Also, this script will choose the longest protein sequences for each gene.
  (gencode-longest_prot.py)


## MODtree based on EnsEMBL compara database. 

1. Download files from EnsEMBL FTP site (download-ens_compara.sh)

2. Prepare EnsEMBL MODtree sequences (ens_compara-to-MODtree.py).
   Usage: ens_compara-to-MODtree.py <downloaded ensembl compara directory> <ensembl version>

3. Combine GENCODE sequences to EnsEMBL MODtree sequences. 

4. Run all-against-all DIAMOND (run-self-diamond.sh).

## MODtree based on EggNOG 5.0 database. 

1. Download files from EggNOG FTP site (download-eggNOG50.sh).

2. Prepare EggNOG MODtree sequences (eggNOG50-to-MODtree.py).
   Usage: eggNOG50-to-MODtree.py <downloaded eggNOG50 directory>

3. Combine GENCODE sequences to EggNOG MODtree sequences.

4. Run all-against-all BLASTP/DIAMOND (run-self-diamond.sh)

