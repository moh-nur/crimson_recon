import argparse
import datetime
import re
import socket
import sys
import time

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", help="Masscan produced results file",
                    required=True)

args = parser.parse_args()

ts = time.time()
sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S')
print("Started mass banner grab @ "+ sttime)

with open(args.file) as fp:
	s = socket.socket()
	s.settimeout(1)
	line = fp.readline()
	while line:
		line = line.strip('\n')

		regEx = r"Discovered open port ([0-9]+)\/tcp on (\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b)"
		m = re.search(regEx, line)
		if m:
			port = int(m.group(1))
			ip = m.group(2)
			#print(ip + ":" + str(port))
			try:
				s.connect((ip, port))
				result = s.recv(10000)
			except:
				pass
			else:
				print("[" + ip + ":" + str(port) + "]\t" + str(result))
			finally:
				s.close()
				s = socket.socket()
				s.settimeout(1)
		line = fp.readline()
