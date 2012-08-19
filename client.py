"""This script do POST request on SERV_ADDR containing some data about commit."""

import hashlib
import json
import requests
import sys
import time

SERV_ADDR = 'http://localhost:13000'

if '--help' in sys.argv:
	print """Usage:
	client.py <repository> <branch> <commit>

	OR

	client.py <command>

	List of commands:
		stop - stop the server"""
	sys.exit(0)

# Command list, can be extended
commands = ['stop']

# Analysing arguments
argc = len(sys.argv)
if argc == 2:
	if sys.argv[1] in commands:
		command = sys.argv[1] 
	else:
		print "Incorrect command"
		sys.exit(1)
	payload = {'command': command}	
elif argc == 4:
	repo = sys.argv[1]
	branch = sys.argv[2]
	commit = sys.argv[3]
	t = time.time()
	hash_ = hashlib.sha256()
	hash_.update(commit + str(t))
	h = hash_.hexdigest()
	info = {'hash': h, 'repo': repo, 'branch': branch, 'commit': commit, 'time': time.asctime()}
	# Commit info -> json format
	info = json.dumps(info)
	payload = {'info': info}
else:
	print "Incorrect input"
	sys.exit(1)

# Make request
r = requests.post(SERV_ADDR, data=payload)
if r.status_code == 200:
	print "Everything is OK"
else:
	print "Oops... We have some problems."
sys.exit(0)