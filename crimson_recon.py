import sys
import argparse
import subprocess
import pathlib
import requests
from bs4 import BeautifulSoup

# From ghostlulz: https://github.com/ghostlulzhacks/CertificateTransparencyLogs
class crtShClass():

	def __init__(self,domain):
		self.url = "https://crt.sh/?q=%25."+domain
		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
		self.cookies = {}
		self.foundURLsList = []

	def subdomainScrape(self):
		r = requests.get(self.url,headers=self.headers,timeout=10)
		soup = BeautifulSoup(r.content,'html.parser')

		tableRows = soup.find_all('table')[2].find_all('tr')

		for row in tableRows:
			try:
				subdomain = row.find_all('td')[4].text
				subdomain = subdomain.replace("*.","")
				if subdomain not in self.foundURLsList:
					self.foundURLsList.append(subdomain)
			except Exception as e:
				pass

	def run(self):
		self.subdomainScrape()

	def printSubdomains(self):
		for subdomain in self.foundURLsList:
			print(subdomain)

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

subdomainList = list()
for domain in domainSet:
	crtsh = crtShClass(domain)
	crtsh.run()
	subdomainList += crtsh.foundURLsList

subdomainSet = set(list(filter(None, subdomainList)))
print(subdomainSet)

