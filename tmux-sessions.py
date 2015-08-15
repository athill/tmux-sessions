from subprocess import call
import sys

# Config for tmux sessions
from simplesampleconfig import sessions

# handle command line args
if len(sys.argv) != 2:
	print('Usage: tmux-sessions.py <session>.\nAvaiable sessions are: ' + ', '.join(sessions.keys()))
	exit()

sessionname = sys.argv[1]

if (sessionname not in sessions):
	print('Error: Session "'+sessionname+'" not found in sessions.\nAvailable sessions are: ' + ', '.join(sessions.keys()))
	exit()


# start session
# tmux -2 new-session -d -s <session-name>
# -2 = support 256 colors
# -d = start as a detached session and attach later 
call(['tmux', '-2', 'new-session', '-d', '-s', sessionname])

# create windows/panes
for i, window in enumerate(sessions[sessionname]):
	# add new window
	# tmux new-window -t <session-name>:<window-index> -n <window-name>
	call(['tmux', 'new-window', '-t', sessionname+':'+str(i+1), '-n', window['name']])
	if len(window['panes']) != 2:
		raise ValueError('Config error: '+sessionname+'['+str(i)+'] must be a list of length 2')
	# split the window vertically
	call(['tmux', 'split-window', '-v'])
	for j, pane in enumerate(window['panes']):
		# select pane in current window
		# tmux select-pane -t <pane-index>
		call(['tmux', 'select-pane', '-t', str(j)])
		# send ssh command
		call(['tmux', 'send-keys', pane, 'C-m'])


# Set default window
# tmux select-window -t <session-name>:<window-index>
call(['tmux', 'select-window', '-t', sessionname+':1'])

# Attach to session
# tmux -2 attach-session -t <session-name>
call(['tmux', '-2', 'attach-session', '-t', sessionname])