import requests, io, os, shutil

#Update for 1.7
def saveFile(filePath, content):
	f = io.open(filePath, mode="w", encoding="utf-8")
	f.write(content)
	f.close()

def update_lib():
	
	splib = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/main/splib.py')
	saveFile('splib.py', splib.text)
	
	account = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/master/account.json')
	saveFile('./data/account.json', account.text)
	
