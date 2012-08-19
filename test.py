"""Test server.py."""

import hashlib
import json
import requests
import sys
import threading
import time
import tserver
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
		branch = 'Branch_Test'
		commit = 'Commit_Test'
		t = time.time()
		tm = time.asctime()
		hash_ = hashlib.sha256()
		hash_.update(commit + str(t))
		h = hash_.hexdigest()
		info = json.dumps({'hash': h, 'repo': repo, 'branch': branch, 'commit': commit, 'time': tm})
		payload = {'info': info}
		r = requests.post('http://localhost:13000', data=payload)
		self.assertEqual(tserver.MyHandler.debug_info, ' START: Server Time: ' + time.asctime() + '\nClient time: %s\
            \nHash: %s\nRepo: %s, Branch: %s\nCommit: %s\nEND\n' % (tm, h, repo, branch, commit))
	
	def tearDown(self):
		"""Shutdown the server using command 'stop'."""

		r = requests.post('http://localhost:13000', data={'command': 'stop'})

if __name__ == '__main__':
        unittest.main()
	sys.exit(0)
