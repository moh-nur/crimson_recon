#!/bin/bash
input=$1
h='HOME'
home=${!h}

echo "Testing all subdomains for http request smuggling"
outputFile=$(echo $1 | cut -d \. -f 1)

rm -f ${outputFile}_smuggler.txt
rm -f ${outputFile}_https.txt

sed 's/^/https:\/\//' ${input} > ${outputFile}_https.txt

python3 $home/tools/pentest-tools/smuggler.py -u ${outputFile}_https.txt -v 1 -t 10 >> ${outputFile}_smuggler.txt


