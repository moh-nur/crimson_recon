import sys
import argparse
import subprocess
import pathlib
import requests
import re
import os
import time
import datetime
from bs4 import BeautifulSoup

ts = time.time()
sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S')
print("Started crimson recon @ "+ sttime)

resultsDir = str(os.getcwd())+"/results"
wordlistFolder = str(os.getcwd())+"/wordlists"
if not os.path.exists(resultsDir):
    os.makedirs(resultsDir)

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--domain", help="Domain to perform recon on",
                    required=True)

parser.add_argument("-i", "--inscope", help="In-scope regex file")
parser.add_argument("-o", "--outscope", help="Out-scope regex file")
parser.add_argument("-na", "--noasn", action='store_true', help="Skip ASN parsing")

args = parser.parse_args()

print ("Parsing: " + args.domain)

name = (args.domain.split("."))[0]
inscopeList = list()
if args.inscope:
	with open(args.inscope) as fp:
		inscopeList += fp.read().splitlines() 

outscopeList = list()
if args.outscope:
	with open(args.outscope) as fp:
		outscopeList += fp.read().splitlines() 

companyDir = resultsDir+"/"+name
if not os.path.exists(companyDir):
    os.makedirs(companyDir)

amassDir = str(pathlib.Path.home())+"/tools/amass"
altdnsDir = str(pathlib.Path.home())+"/tools/altdns/altdns"
if not args.noasn:
	print ("Retrieving asn list")
	process = subprocess.run([amassDir+"/amass intel -org "+name],
							cwd=amassDir,
							shell=True,
	                         stdout=subprocess.PIPE, 
	                         universal_newlines=True)

	asnList = process.stdout.split("\n")
	asnResults = companyDir+"/"+name+"_asns.txt"
	with open(asnResults, 'w') as f:
	    for asn in asnList:
	        f.write("%s\n" % asn)
	print("asn found: ==> " + str(asnList))

	cidrList = list()
	domainList = list()

	print ("Retrieving cidr for each asn found")
	for asn in asnList:
		print ("Processing asn: ==> "+asn)
		asnNumber = (asn.split(","))[0]

		regEx = "([0-9.]+){4}/[0-9]+"
		whoisCommand = "whois -h whois.radb.net -- '-i origin "+asnNumber+" ' | grep -Eo \""+regEx+"\" | sort -u"
		whoProcess = subprocess.run([whoisCommand],
							shell=True,
	                         stdout=subprocess.PIPE, 
	                         universal_newlines=True)

		cidrArray = whoProcess.stdout.split("\n")
		cidrList += cidrArray

		amassProcess = subprocess.run([amassDir+"/amass intel -asn "+asnNumber],
							cwd=amassDir,
							shell=True,
	                         stdout=subprocess.PIPE, 
	                         universal_newlines=True)
		asnDomainList = amassProcess.stdout.split("\n")
		domainList+=asnDomainList
		print("asnDomainList: "+asn+"==> "+str(asnDomainList))
		#break

	cidrSet = set(list(filter(None, cidrList)))
	cidrResults = companyDir+"/"+name+"_cidrs.txt"
	with open(cidrResults, 'w') as f:
	    for cidr in cidrSet:
	        f.write("%s\n" % cidr)
	print("cidr: ==> "+str(cidrSet))

	print ("Retrieving subdomains for each cidr")
	for cidr in cidrSet:
		amassProcess = subprocess.run([amassDir+"/amass intel -cidr "+cidr],
							cwd=amassDir,
							shell=True,
	                         stdout=subprocess.PIPE, 
	                         universal_newlines=True)
		cidrDomainList = amassProcess.stdout.split("\n")
		domainList+=cidrDomainList
		print("cidrDomainList: "+cidr+"==> "+str(cidrDomainList))
		#break

	domainSet = set(list(filter(None, domainList)))
	print ("Found domains ==> "+str(domainSet))

	if inscopeList or outscopeList:
		print ("Filtering out of scope domains")
		removalCandidates = list()
		for domain in domainSet:
			if outscopeList and not inscopeList:
				inScope = True
			else:
				inScope = False

			if inscopeList:
				for scope in inscopeList:
					m = re.search(scope, domain)
					if m:
						inScope = True
						break

			if outscopeList:
				for scope in outscopeList:
					m = re.search(scope, domain)
					if m:
						inScope = False
						break

			if not inScope:
				removalCandidates.append(domain)
		for removalDomain in removalCandidates:
			domainSet.remove(removalDomain)

	print(domainSet)
else:
	print ("Skipping asn asset discovery")

subdomainList = list()

# print ("passively scraping subdomains using amass enum")
# amassProcess = subprocess.run([amassDir+"/amass enum -passive -d "+args.domain],
# 					cwd=amassDir,
# 					shell=True,
#                      stdout=subprocess.PIPE, 
#                      universal_newlines=True)
# amassSubdomainList = amassProcess.stdout.split("\n")
# subdomainList+=amassSubdomainList

print ("Brute forcing domain names using gobuster")
process = subprocess.run(["gobuster dns -d "+args.domain+" -z -q -w "+wordlistFolder+"/subdomains-top1million-5000.txt"],
						shell=True,
                         stdout=subprocess.PIPE, 
                         universal_newlines=True)

gobustedSubdomains = process.stdout.split("\n")
print (gobustedSubdomains)
for goDomain in gobustedSubdomains:
	m = re.search('Found: (.*)', goDomain)
	if m:
		subdomainList.append(m.group(1))

subdomainSet = set(list(filter(None, subdomainList)))
print ("Found subdomains")
if inscopeList or outscopeList:
	print ("Filtering out of scope subdomains")
	removalCandidates = list()
	for domain in subdomainSet:
		if outscopeList and not inscopeList:
			inScope = True
		else:
			inScope = False

		if inscopeList:
			for scope in inscopeList:
				m = re.search(scope, domain)
				if m:
					inScope = True
					break

		if outscopeList:
			for scope in outscopeList:
				m = re.search(scope, domain)
				if m:
					inScope = False
					break

		if not inScope:
			removalCandidates.append(domain)
	for removalDomain in removalCandidates:
		subdomainSet.remove(removalDomain)

print("Filtered subdomain list")
print(subdomainSet)

companyDir = resultsDir+"/"+name
if not os.path.exists(companyDir):
    os.makedirs(companyDir)

if not args.noasn:
	domainResults = companyDir+"/"+name+"_domains.txt"
	with open(domainResults, 'w') as f:
	    for domain in domainSet:
	        f.write("%s\n" % domain)

subDomainResults = companyDir+"/"+name+"_subdomains.txt"
with open(subDomainResults, 'w') as f:
    for subdomain in subdomainSet:
        f.write("%s\n" % subdomain)

premutations = companyDir+"/"+name+"_premutations.txt"
additionalsubDomains = companyDir+"/"+name+"_subdomains_altdns.txt"
print ("Brute forcing additional subdomains using altdns premutations")
process = subprocess.run(["python3 "+ altdnsDir +" -i " + subDomainResults +" -o "+ premutations + " -w " + wordlistFolder + "/altdns_words.txt -r -s " + additionalsubDomains],
						shell=True,
                         stdout=subprocess.PIPE, 
                         universal_newlines=True)

os.remove(premutations)

ts = time.time()
sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')
with open(companyDir+"/"+name+"_lastrun.txt", 'w') as f:
	f.write(sttime+"\n")
