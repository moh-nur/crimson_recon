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
``~/tools/EyeWitness/EyeWitness.py -f [FILE] --web
