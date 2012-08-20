#!/usr/bin/python
"""This script do POST request on SERV_ADDR containing some data about commit."""

import json
import os
import re
import requests
import subprocess
import sys
import time

SERV_ADDR = 'http://localhost:13000'

def git(args):
	"""Work with git via program."""

	args = ['git'] + args
	git = subprocess.Popen(args, stdout = subprocess.PIPE)
	details = git.stdout.read()
	details = details.strip()
	return details

def get_repo_name():
	"""Get repository name."""

	if git(['rev-parse', '--is-bare-repository']) == 'true':
		name = os.path.basename(os.getcwd())
		if name.endswith('.git'):
			name = name[:-4]
		return name
	else:
		return os.path.basename(os.path.dirname(os.getcwd()))

def get_info():
	"""Get additional information about commit."""
	details = git(['show', '--pretty=format:%s%n%H%n%cd'])
	details = details.split('\n')
	inf = re.findall(r"'.+'|https://.+", details[0])
	inf.extend(details[1:])
	return inf

if '--help' in sys.argv:
	print """Usage:
	client.py

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
elif argc == 1:
	inform = get_info()
	repo = get_repo_name()
	repo_url = inform[1]
	branch = inform[0][1:-1]
	commit_hash = inform[2]
	t = inform[3]
	info = {'commit_hash': commit_hash, 'repo_url': repo_url, 'repo': repo, 'branch': branch,  'time': t}
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
