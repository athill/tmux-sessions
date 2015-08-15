# This sets up one session with two windows, 
demo = 'echo "*** THIS IS JUST A DEMO ***"; '

sessions = {
	'app': [
		{
			'name': 'local',
			'panes': [
				demo+'cd /path/to/app; gulp watch',
				demo+'mysql -u user -p app'
			]
		},
		{
			'name': 'remote',
			'panes': [
				demo+'ssh -t user@webhost.com "cd /path/to/app/logs; bash --login"',
				demo+'ssh -t user@dbhost.com "mysql -u user -p app; bash --login"'
			]
		}		
	]
}