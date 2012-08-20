#!/usr/bin/python
"""Test for server.py."""

import json
import requests
import sys
import threading
import time
import tserver_lin as tserver
import unittest


class TestServer(unittest.TestCase):
	"""Test class."""

	def setUp(self):
		"""Start the server in new thread."""

		if not tserver.DEBUG:
			print "Debug mode is turned off. Set tserver.DEBUG True."
			sys.exit(0)
		print "Trying to start server."
		p1 = threading.Thread(target=tserver.run, name="Server")
		p1.start()
	
	def test_server(self):
		"""Send POST request containing some commit info."""

		repo = 'Repo_Test'
		repo_url = 'https://test_url'
		branch = 'Branch_Test'
		t = time.asctime()
		commit_hash = '1234567890abcdef'
		dt = {'commit_hash': commit_hash, 'repo_url': repo_url, 'repo': repo, 'branch': branch,  'time': t}
		info = json.dumps(dt)
		payload = {'info': info}
		r = requests.post('http://localhost:13000', data=payload)
		self.assertEqual(tserver.MyHandler.debug_info, ' START: Server Time: ' + time.asctime() + '\nRepo url: %(repo_url)s\
            \nRepo: %(repo)s\nBranch: %(branch)s\nHash: %(commit_hash)s\nCommit time: %(time)s\nEND\n' % dt)
	
	def tearDown(self):
		"""Shutdown the server using command 'stop'."""

		r = requests.post('http://localhost:13000', data={'command': 'stop'})

if __name__ == '__main__':
        unittest.main()
	sys.exit(0)
