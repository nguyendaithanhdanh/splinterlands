import requests, io, os, shutil

def update_lib():
	obb = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/main/splib.py')
	saveFile('/data/lib/splib.py', obb)
	data_team = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/main/team.json')
	saveFile('../team.json')
	os.remove('splib.py')
	shutil.rmtree('__pycache__') 
	os.remove('update.py')
