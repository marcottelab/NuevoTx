#!/bin/bash
ID_LIST=$1

CUR_DIR=$(dirname $0)

if [ ! -e $ID_LIST ]; then
  echo $ID_LIST "is not available. Exit."
  exit

else
  SP_LIST=$(echo $ID_LIST | awk -F"." '{print $1}')
  VERSION=$(echo $ID_LIST | awk -F"." '{print $3}')
  
  TX_ALL=$SP_LIST".tx.all."$VERSION".fa.gz"
  TX_FINAL=$SP_LIST".tx."$VERSION".fa"
  echo $TX_ALL $TX_FINAL
  $CUR_DIR/annot-final_fa.py $ID_LIST $TX_ALL tx > $TX_FINAL

  CDS_ALL=$SP_LIST".cds.all."$VERSION".fa.gz"
  CDS_FINAL=$SP_LIST".cds."$VERSION".fa"
  echo $CDS_ALL $CDS_FINAL
  $CUR_DIR/annot-final_fa.py $ID_LIST $CDS_ALL cds > $CDS_FINAL
  
  PROT_ALL=$SP_LIST".prot.all."$VERSION".fa.gz"
  PROT_FINAL=$SP_LIST".prot."$VERSION".fa"
  echo $PROT_ALL $PROT_FINAL
  $CUR_DIR/annot-final_fa.py $ID_LIST $PROT_ALL prot > $PROT_FINAL
fi
