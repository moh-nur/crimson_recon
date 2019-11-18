import json, sys , re
from codecs import encode, decode

with open('scope.json') as json_file:
    data = json.load(json_file)
    scope = data['target']['scope']['include']

    p = re.compile("[a-z]")
    for s in scope:
    	if(s['enabled'] == True and "h1" not in s['host']):
    		matchHost = decode(encode(s['host'], 'latin-1', 'backslashreplace'), 'unicode-escape')
    		matchFile = decode(encode(s['file'], 'latin-1', 'backslashreplace'), 'unicode-escape')
    		matchFile = matchFile.replace(".*.*",".*")
    		matchHost = matchHost.replace("$","")
    		matchFile = matchFile.replace(".*.*",".*")
    		matchFile = matchFile.replace("^/","\\") + "$"
    		scopeRegex = matchHost+matchFile
    		print (scopeRegex)

    		wildcardRegex = "\\.\\*"
    		p = re.compile(wildcardRegex)
    		for m in p.finditer(scopeRegex):
    			print(m.start(), m.group())
    		
    		#sys.exit()

