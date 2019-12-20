#!/bin/bash
for SF in $(ls */quant.sf)
do
  OUT=${SF/\/quant.sf/}".sf"
  echo $SF $OUT
  cp $SF $OUT
done
