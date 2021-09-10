import requests, io, os, shutil

def saveFile(filePath, content):
	f = io.open(filePath, mode="w", encoding="utf-8")
	f.write(content)
	f.close()

def update_lib():
	os.mkdir('./data/lib')
	os.chdir('./data/lib')
	f=open('update.py','w')
	f.close()
	obb = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/main/splib.py')
	saveFile('splib.py', obb.text)
	data_team = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/main/team.json')
	saveFile('../team.json', data_team.text)
	os.chdir('../../')
	main = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/main/team_manage.py')
	saveFile('team_manage.py', main.text)
	os.remove('splib.py')
	shutil.rmtree('__pycache__') 
	os.remove('update.py')
