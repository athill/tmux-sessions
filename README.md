# tmux-sessions

## Requirements: 

[tmux](https://tmux.github.io/), bash, [python](https://www.python.org/) (2 or 3), [jq](https://stedolan.github.io/jq/) if you want to query

## Purpose

At my job, I sometimes have to access the command line of (ssh into) several servers at a time to view logs, verify configuration changes, etc. This script allows me to log into all the relavant servers for a given environment and even run some setup commands before I begin interacting with the servers (after I log in).

## Usage

To run:
	
	python tmux-sessions.py {session}

This will open a multiplex session with the windows and panes defined in {session}

The sessions are defined in config.py. The `sessions` variable defined in config.py is expected to be a data structure of the form:

	{
		'session1': [
			{
				'panes': [
					'ssh -t server1.example.com "cd /var/app/logs/; bash --login"',
					'ssh -t server2.example.com "cd /var/app/logs/; bash --login"',
				],
				'name': 'window1'
			},
			...
		],
		...
	}

Each session represents a list of windows. Each window has a name and a list of exactly two commands to issue in the panes within the window. What you end up with is a tmux session with all the windows you define and two panes (split vertically) per window.

Example configuration files can be found in simplesampleconfig.py and advancedsampleconfig.py.

**Note:** You must have a config.py file, which is not included.  


Full `tmux` documentation is avaialable on the [man page](http://www.openbsd.org/cgi-bin/man.cgi?query=tmux&sektion=1).

All `tmux` commands are preceded by a prefix, which, by default, is `Ctrl-b`.

### Window Navigation: 

1. [prefix] + [number]   (e.g., `Ctrl-b 2, for the second window)
2. [prefix] + p Previous window
3. [prefix] + n Next window

### Pane navigation

1. [prefix] + o Switch panes
2. [prefix] + q Briefly show numeric values of panes. You can then hit the number to switch to the selected pane

### Quitting

* `[prefix] + d` gets you out of a given session and back to the command line
* `$ tmux session-kill` kills the most recent session
* `$ tmux list-sessions` lists the current sessions
* `$ tmux kill-session <session-name>` kills the selected session

### More on `tmux`

More instructions on session/window/pane manipulation or link to a good [cheatsheet](http://www.dayid.org/os/notes/tm.html) and/or [tutorial](http://blog.hawkhost.com/2010/06/28/tmux-the-terminal-multiplexer/)

## Querying

If you have `jq` installed, you can query the sessions

### Usage

	python query-sessions <valid-jq-query>

For example, `python query-sessions.py '.app[] | .name'` would list all the window names in the "app" session
