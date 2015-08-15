from subprocess import call
import sys
import json
import os

# Config for tmux sessions
from config import sessions

# handle command line args
if len(sys.argv) != 2:
	print('Usage: query-sessions.py <valid-jq-query>.\nAvaiable sessions are: ' + ', '.join(sessions.keys()))
	exit()

tmpfile = 'tmp.json'
out_file = open(tmpfile, 'w')
json.dump(sessions, out_file)
out_file.close()

commandlist = ['jq', '-r'] + sys.argv[1:]
commandlist.append(tmpfile)
call(commandlist)

os.remove(tmpfile)