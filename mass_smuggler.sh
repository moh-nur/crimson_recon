#!/bin/bash
input=$1
h='HOME'
home=${!h}

echo "Testing all subdomains for http request smuggling"
outputFile=$(echo $1 | cut -d \. -f 1)
echo $outputFile
while IFS= read -r line
do
  $(python3 $home/tools/pentest-tools/smuggler.py -u https://$line/ -v 1 -t 10 >> ${outputFile}_smuggler.txt)
done < "$input"

