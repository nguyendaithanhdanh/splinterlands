import requests, io, os, shutil

#Update for 1.7
def saveFile(filePath, content):
	f = io.open(filePath, mode="w", encoding="utf-8")
	f.write(content)
	f.close()

def update_lib():
	
	splib = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/main/team_manage.py')
	saveFile('team_manage.py', splib.text)
