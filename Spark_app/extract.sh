#!/bin/bash

for year in {2002..2016}
do 
  while read location; do 
	path="ftp://ftp.ncdc.noaa.gov/pub/data/noaa/$year/$location-$year.gz"
	wget $path
  done <newba.txt
done 
