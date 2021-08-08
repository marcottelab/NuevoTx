# MODtree: the reference for NuevoTx

## MODtree from EnsEMBL compara database. 

1. Download files from EnsEMBL FTP site (download-ens_compara.sh)

2. Prepare EnsEMBL MODtree sequences (ens_compara-to-MODtree.py).
   Usage: ens_compara-to-MODtree.py <downloaded ensembl compara directory> <ensembl version>

3. Download files from GENCODE website. 

4. Convert the header of GENCODE FASTA files compatible to MODtree.
  Also, this script will choose the longest protein sequences for each gene.
  (gencode-longest_prot.py)

5. Combine GENCODE sequences EnsEMBL MODtree sequences. 
  $ cp MODtree_ens_compara

6. Run all-against-all DIAMOND (run-self-diamond.sh).

## MODtree from EggNOG 5.0 database. 


1. Download files from EggNOG FTP site (download-eggNOG50.sh).

2. Prepare EggNOG MODtree sequences (eggNOG50-to-MODtree.py).
   Usage: eggNOG50-to-MODtree.py <downloaded eggNOG50 directory>
