import requests, io, os, shutil

#Update for 1.2
def saveFile(filePath, content):
	f = io.open(filePath, mode="w", encoding="utf-8")
	f.write(content)
	f.close()

def update_lib():

	obb = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/main/splib.py')
	saveFile('splib.py', obb.text)
	try:
		import PyQt5
	except Exception as e:
		os.system('pip install PyQt5')
