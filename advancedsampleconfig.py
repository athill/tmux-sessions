import re
import pprint

pp = pprint.PrettyPrinter(indent=4)

app = 'app'

__sessions = {
	app+'-prd': {
		'windows': [
			{'name': 'WEB1', 'panes': ['1', '2'] },
			{'name': 'WEB2', 'panes': ['3', '4'] },
			{'name': 'WEB3', 'panes': ['5', '6'] },
			{'name': 'BUS', 'panes': ['7', '8'] },
			{'name': 'DB', 'panes': ['9', '10'] }, 
		],
		'server': ['server%s.example.com', 'pane']
	}
}

# Build up test environments
__testenvs = ['snd', 'cnv', 'unt', 'reg', 'stg']
__windows = [
	{'name': 'WEB', 'panes': ['11', '12'] },
	{'name': 'BUS', 'panes': ['13', '14'] },
	{'name': 'DB', 'panes': ['15', '16'] }
]
for env in __testenvs:
	sessionname = app+'-'+env
	__sessions[sessionname] = {
		'windows': __windows,
		'server': ['server%s.example.com', 'pane']
	}
# add commands to all sessions
for session in __sessions:
	__sessions[session]['commands'] = [
		# cd to log directory
		['cd /opt/apps/logs/%s/%s',
			 # get app from name
			{'func': lambda name: re.sub(r'^(\w+)\d+', r'\1', name).lower(), 'args': ['name']}, 
			# get env from session
			{'func': lambda session: re.sub(r'^\w+-(.*)', r'\1' ,session), 'args': ['env']}]
	]

def __getValueFromScope(key, scope):
	"retrieve value of keyword in scope (based on scope when building `sessions` below)"
	if key == 'pane':
		return scope['pane']
	elif key == 'name':
		return scope['window']['name']
	elif key == 'env':
		return scope['session']


def __applyTemplate(template, subs, scope):
	"interpolate template with appropriate current values"
	args = []
	for sub in subs:
		if isinstance(sub, dict):
			# call the method with spread arguments
			args.append(sub['func'](*[__getValueFromScope(s, scope) for s in sub['args']]))
		else:
			# Just retrieve the value
			args.append(__getValueFromScope(sub, scope))
	return template % tuple(args)



def __getCommands(server, commandList, scope):
	"Build up command string to pass to pane"
	def getCommand(cmd, scope):
		"interpolate commands with values"
		if (isinstance(cmd, list)):
			return __applyTemplate(cmd[0], cmd[1:], scope)
		else:
			return cmd
	# -t to pass commands to shell
	pane = 'ssh -t ' + getCommand(server, scope)
	commands = [getCommand(command, scope) for command in commandList]
	# log in to shell, rather than terminate session
	commands.append('bash --login')
	pane = pane + ' "' + '; '.join(commands) + '"'
	return pane


sessions = {}
for session in __sessions:
	__session = __sessions[session]
	sessions[session] = [{
		'name': window['name'] + ':' + ','.join(window['panes']),
		'panes': [__getCommands(__session['server'], __session['commands'], locals()) for pane in window['panes']]
	} for window in __session['windows']]

