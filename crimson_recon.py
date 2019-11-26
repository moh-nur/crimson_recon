import sys, argparse, subprocess, pathlib

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--domain", help="Domain to perform recon on",
                    required=True)

parser.add_argument("-i", "--inscope", help="In-scope regex file")
parser.add_argument("-o", "--outscope", help="Out-scope regex file")

args = parser.parse_args()

print ("Parsing: " + args.domain)

name = (args.domain.split("."))[0]

print(name)
print(pathlib.Path.home())

amassDir = f"{str(pathlib.Path.home())}/tools/amass/"
process = subprocess.run([f"{amassDir}amass intel -org {name}"],
						cwd=amassDir,
						shell=True,
                         stdout=subprocess.PIPE, 
                         universal_newlines=True)

asnList = process.stdout.split("\n")
print(asnList)

cidrList = list()
domainList = list()

for asn in asnList:
	print (asn)
	asnNumber = (asn.split(","))[0]

	regEx = "([0-9.]+){4}/[0-9]+"
	whoisCommand = f"whois -h whois.radb.net -- '-i origin {asnNumber} ' | grep -Eo \"{regEx}\" | sort -u"
	whoProcess = subprocess.run([whoisCommand],
						shell=True,
                         stdout=subprocess.PIPE, 
                         universal_newlines=True)

	cidrArray = whoProcess.stdout.split("\n")
	cidrList += cidrArray

	amassProcess = subprocess.run([f"{amassDir}amass intel -asn {asnNumber}"],
						cwd=amassDir,
						shell=True,
                         stdout=subprocess.PIPE, 
                         universal_newlines=True)
	asnDomainList = amassProcess.stdout.split("\n")
	domainList += asnDomainList
	print(asnDomainList)
	break

cidrSet = set(list(filter(None, cidrList)))
print(cidrSet)

for cidr in cidrSet:
	amassProcess = subprocess.run([f"{amassDir}amass intel -cidr {cidr}"],
						cwd=amassDir,
						shell=True,
                         stdout=subprocess.PIPE, 
                         universal_newlines=True)
	cidrDomainList = amassProcess.stdout.split("\n")
	domainList += cidrDomainList
	print(cidrDomainList)
	break

domainSet = set(list(filter(None, domainList)))
print(domainSet)