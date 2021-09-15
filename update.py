import requests, io, os, shutil

#Update for 1.3
def saveFile(filePath, content):
	f = io.open(filePath, mode="w", encoding="utf-8")
	f.write(content)
	f.close()

def update_lib():
	
	obb = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/main/splib.py')
	saveFile('splib.py', obb.text)
