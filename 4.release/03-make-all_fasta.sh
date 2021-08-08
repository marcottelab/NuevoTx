#!/bin/bash

CUR_DIR=$(dirname $0)
VERSION=$CUR_DIR/../"VERSION.conf"
source $VERSION

DIR_NAME=$(dirname $PWD)
SP_NAME=$(basename $DIR_NAME)
echo $SP_NAME


PROT_ALL=$SP_NAME".prot.all."$VERSION".fa"
echo $PROT_ALL
zcat ../tx.raw/*prot.raw.fa.gz > $PROT_ALL

CDS_ALL=$SP_NAME".cds.all."$VERSION".fa"
echo $CDS_ALL
zcat ../tx.raw/*CDS.raw.fa.gz > $CDS_ALL

TX_ALL=$SP_NAME".tx.all."$VERSION".fa"
echo $TX_ALL
zcat ../tx.raw/*.tx.orient.fa.gz > $TX_ALL

