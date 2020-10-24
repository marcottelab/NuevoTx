#!/bin/bash
for TSV in $(ls */abundance.tsv)
do
  TSV_OUT=${TSV/\/abundance.tsv/}".tsv"
  echo $TSV $TSV_OUT
  cp $TSV $TSV_OUT

  H5=${TSV/.tsv/}".h5"
  H5_OUT=${H5/\/abundance.h5/}".h5"
  echo $H5 $H5_OUT
  cp $H5 $H5_OUT

  LOG=${TSV/abundance.tsv/run_info.json}
  LOG_OUT=${TSV/\/abundance.tsv/}".log"
  echo $LOG $LOG_OUT
  cp $LOG $LOG_OUT
done

