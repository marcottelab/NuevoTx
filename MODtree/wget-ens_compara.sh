#!/bin/bash

ENS_VERSION="100"

wget http://ftp.ensembl.org/pub/release-$ENS_VERSION/compara/species_trees/vertebrates_species-tree_Ensembl.nh
wget -O "vertebrates_species-tree_NCBI_Taxonomy.nh" http://ftp.ensembl.org/pub/release-$ENS_VERSION/compara/species_trees/vertebrates_species-tree_NCBI%20Taxonomy.nh
wget http://ftp.ensembl.org/pub/release-$ENS_VERSION/emf/ensembl-compara/homologies/Compara.$ENS_VERSION.protein_default.aa.fasta.gz
wget http://ftp.ensembl.org/pub/release-$ENS_VERSION/emf/ensembl-compara/homologies/Compara.$ENS_VERSION.protein_default.cds.fasta.gz
wget http://ftp.ensembl.org/pub/release-$ENS_VERSION/emf/ensembl-compara/homologies/Compara.$ENS_VERSION.protein_default.nh.emf.gz
