#!/bin/bash
for SF in $(ls */quant.sf)
do
  SF_OUT=${SF/\/quant.sf/}".sf"
  echo $SF $SF_OUT
  cp $SF $OUT

  LOG=${SF/\/quant.sf/}"/logs/salmon_quant.log"
  LOG_OUT=${SF/\/quant.sf/}".log"
  echo $LOG $LOG_OUT
  cp $LOG $LOG_OUT
done

