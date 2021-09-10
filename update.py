import requests, io, os, shutil

def saveFile(filePath, content):
	f = io.open(filePath, mode="w", encoding="utf-8")
	f.write(content)
	f.close()

def update_lib():
	obb = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/main/splib_beta.py')
	saveFile('/data/lib/splib.py', obb)
	data_team = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/main/team.json')
	saveFile('../team.json')
	os.remove('splib.py')
	shutil.rmtree('__pycache__') 
	os.remove('update.py')
