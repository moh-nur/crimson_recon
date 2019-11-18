import json, sys , re
from codecs import encode, decode
from ast import literal_eval

#def enumerate(input):
	
no_regex = str.maketrans("", "", "$^\\")
scopeList = set()

with open('scope.json') as json_file:
	data = json.load(json_file)
	scope = data['target']['scope']['include']

	p = re.compile("[a-z]")
	for s in scope:
		# Don't parse scopes that need to be created
		if(s['enabled'] == True and ("h1" not in s['host'] and "h1" not in s['file'])):
			#Remove escape characters and normalize scope regex
			matchHost = decode(encode(s['host'], 'latin-1', 'backslashreplace'), 'unicode-escape')
			matchFile = decode(encode(s['file'], 'latin-1', 'backslashreplace'), 'unicode-escape')
			matchFile = matchFile.replace(".*.*",".*").replace(".*.*",".*").replace("^/","\\/").replace("//","/") + "$"
			matchHost = matchHost.replace("$","")
			scopeRegex = matchHost+matchFile
			#print (scopeRegex)
			sanitized = scopeRegex.translate(no_regex)
			sanitized = sanitized.replace(".*","<")
			scopeList.add(s['protocol'] +"://" + sanitized)

#Find number of places to enumerate
for s in scopeList:
	print (s)
	marker = "<"
	p = re.compile(marker)
	for m in p.finditer(s):
		print(m.start(), m.group())

	#sys.exit()

