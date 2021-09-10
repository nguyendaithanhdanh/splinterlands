import request, io

def update_lib():
	obb = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/main/splib.py')
	saveFile('splib.py', obb)
	data_team = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/main/team.json')
	saveFile('../team.json')
