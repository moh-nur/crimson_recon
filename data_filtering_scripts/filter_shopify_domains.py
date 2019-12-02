import urllib.request
import os
import ssl

filepath = "shopify_subdomains.txt"
output_http="shopify_subdomains_filtered_http.txt"
failed_http="shopify_subdomains_failed_connect_http.txt"

output_https="shopify_subdomains_filtered_https.txt"
failed_https="shopify_subdomains_failed_connect_https.txt"


http_filtered = list()
http_notConnecting = list()

https_filtered = list()
https_notConnecting = list()

TIMEOUT=3

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

with open(filepath) as fp:
	line = fp.readline()
	cnt = 1
	while line:
   		
		url = rf"http://{line}"
		print(url)
		try:
			with urllib.request.urlopen(url,timeout=TIMEOUT, context=ctx) as response:
				html = response.read()
				if b"#did-you-mean-link" not in html:
					http_filtered.append(line)
					print("Found valid")
		except IOError:
			http_notConnecting.append(line)

		url = rf"https://{line}"
		try:
			with urllib.request.urlopen(url,timeout=TIMEOUT, context=ctx) as response:
				html = response.read()
				if b"#did-you-mean-link" not in html:
					https_filtered.append(line)
					print("Found valid")
		except IOError:
			https_notConnecting.append(line)
			print("Failed to connect")

		line = fp.readline()

filteredDir = f"{str(os.getcwd())}/filtered"

with open(f"{filteredDir}/shopify_subdomains_filtered_http.txt", 'w') as f:
    for page in http_filtered:
        f.write("%s\n" % page)

with open(f"{filteredDir}/shopify_subdomains_failed_connect_http.txt", 'w') as f:
    for page in http_notConnecting:
        f.write("%s\n" % page)

with open(f"{filteredDir}/shopify_subdomains_filtered_https.txt", 'w') as f:
    for page in https_filtered:
        f.write("%s\n" % page)

with open(f"{filteredDir}/shopify_subdomains_failed_connect_https.txt", 'w') as f:
    for page in https_notConnecting:
        f.write("%s\n" % page)