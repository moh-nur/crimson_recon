# crimson_recon

Script to enumerate domains, and to remove out of scope items using a regex list. Also contains custom scripts to filter enumerated subdomain data even further.

Long term goal is to standarize the enumeration and filtering so that code can be reused

## Useful linux commands

###Use nmap to resolve all subdomains
``nmap -T5 -sL -n -oG resolved -iL "subDomain_List_fileName"``

###Grab all ip addresses from "resolved" file created by nmap

``cat resolved | grep ^Host | cut -d " " -f 2 > masscan.il``

###Use masscan to check ports using file "masscan.il"

``~/tools/masscan/bin/masscan -iL [FILE] --rate 1500 -p0-65535 > masscan.txt ``

###Use EyeWitness to take snapshot of all subdomains

``~/tools/EyeWitness/EyeWitness.py -f [FILE] --web --proxy-ip 127.0.0.1 --proxy-port 8080``

###Retrieve data from VPS

``scp -r [USERID]@[IP]:[SOURCE DIR] [DEST DIR]``

## Useful nmap commands

### Change nmap user agent

``--script-args "[USER AGENT]"``

### Nmap scan all ports + identify service and os

``nmap -p- [IP] -sV -A``

#### Bring it all together

``nmap -p- [IP] -sV -A --script-args http.useragent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36" -v 1``

## Setup golang

### Install (deb based systems)

``sudo apt-get install golang``

### Setup terminal path
#### Edit ~/.bashrc and add the below to the end.
``export GOPATH=$HOME/go``
``export PATH=$PATH:$GOROOT/bin:$GOPATH/bin``
#### Make this change active using source command
``source ~/.bashrc``
