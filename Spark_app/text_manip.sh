#!/bin/bash

dir="/home/ro/Desktop/DataLab"
diro=$dir/$1
for file in $diro/*
do 
	gunzip "$file" 
done 	

for file in $diro/*
do 
	java -classpath $dir ishJava $file $file.out 
	mv $file.out $dir/smaolla6
done 

for file in $dir/smaolla6/*
do 	
	sed '1d' $file >temp; mv temp $file
done

for file in $dir/smaolla6/*
do 	
	awk '{gsub(/T\*/, " "); print $0 }' "$file" > "$file.tmp" && mv "$file.tmp" "$file"


done 

for file in $dir/smaolla6/*
do 	
	rootmp=$( echo $file | cut -d'/' -f 7)
	rootn=$(echo "$rootmp"  | cut -d'-' -f 1,2)
	
	while read p; do
	      read -r -a array <<< $p
	      comp="${array[0]}-${array[1]}"
	      if [ $comp == "$rootn" ]; then
		location="${array[2]}-${array[3]}"
	      	awk -v loc=$location '{print loc,$0}' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
	      fi
	done <"$dir/major_us_stations.txt"

done 

for file in $dir/smaolla6/*
do 

    nrecords=$(wc -l $file | cut -f1 -d' ')
    awk  'NR>1 && NR<$nrecords{print $23} END{print "**"}' "$file" > "$file.tmp" 
    paste -d ' ' <(awk '{print $0}' $file) <(awk '{print $1}' "$file.tmp" ) > "$file-clean"  
    rm "$file" "$file.tmp"
done
