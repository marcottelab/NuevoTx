#!/bin/bash

CUR_DIR=$(dirname $0)
MODTREE_CONF=$CUR_DIR/../"MODtree.conf"
source $MODTREE_CONF

VERSION_CONF=$CUR_DIR/../"VERSION.conf"
source $VERSION_CONF

FA=$1
echo "FA: "$FA
if [ ! -e $FA ]; then
  echo $FA" is not available. Exit."
  exit
fi

SP_NAME=$(echo $FA| awk -F"." '{print $1}')
SP_CONF=$CUR_DIR/../"SPECIES.conf"
SP_CODE=$(grep $SP_NAME $SP_CONF | awk '{print $2}')
echo "SP: "$SP_NAME, $SP_CODE

if [ ! $SP_CODE ]; then
  echo $SP_NAME" is not available. Check SPECIES.conf file. Exit."
  exit
fi

TBL6=$(ls $SP_NAME*tbl6*)
echo "TBL6: "$TBL6
if [ ! -e $TBL6 ]; then
  echo $TBL6" is not available. Exit."
  exit
fi

FILENAME_OUT=$SP_NAME".id_list."$VERSION".txt"
echo "Make "$FILENAME_OUT

$CUR_DIR/make-id_list.py $FA $TBL6 $SP_CODE > $FILENAME_OUT
