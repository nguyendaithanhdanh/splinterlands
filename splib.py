from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import getpass, time, io, json, random, os, requests
from bs4 import BeautifulSoup



version = '0.3'

username = getpass.getuser()

usr_path=('C:/Users/', username, '/AppData/Local/Google/Chrome/User Data')
filePath = ''.join(usr_path)

card_path = './data/card.json'
team_path = './data/team.json'
src_web_path = './data/source_web.html'

with open(card_path) as json_file:
    card = json.load(json_file)
list_card_name = []
for i in card:
	list_card_name.append(i)
list_name = sorted(list_card_name)
mana = 0






def initDriver():
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("user-data-dir="+filePath)
	'''
	prefs = {
	"profile.managed_default_content_settings.images": 2
	}
	chrome_options.add_experimental_option("prefs", prefs)
	'''
	driver = webdriver.Chrome('./data/webdriver/chromedriver', options = chrome_options)
	driver.get('https://splinterlands.com/?p=battle_history') 
	#time.sleep(5)

	#SELECT BATTLE MODE
	driver.execute_script("var roww = document.getElementsByClassName('row')[1].innerHTML;var reg = /HOW TO PLAY|PRACTICE|CHALLENGE|RANKED/;var resultt = roww.match(reg);while(resultt != 'RANKED'){document.getElementsByClassName('slider_btn')[1].click();roww = document.getElementsByClassName('row')[1].innerHTML;resultt = roww.match(reg);};")

	#BATTLE
	driver.execute_script("document.getElementsByClassName('big_category_btn red')[0].click();")

	time.sleep(10)

	#Create team
	driver.execute_script("document.getElementsByClassName('btn btn--create-team')[0].click();")





def checkMana(add):
	mana = 0
	for i in add:
		mana += card[i]['mana']
	return mana


def inputMana():
	mana = input('Mana: ')
	while(not mana.isdigit()):
		os.system('cls')
		print('Opps, try again!')
		mana = input('Mana: ')
	return int(mana)




def menuOpt(select, team_adding):
	global mana
	if (select.isalpha()):
		select = select.upper()
	if (select.isdigit()):
		if(int(select) <= 0 or int(select) > 95):
			select = ''
	while (select != 'S' and select != 'C' and select != 'Q' and select != 'M' and (not select.isdigit())):
		os.system('cls')
		showListName()
		print("\n")
		print(f'Mana: [{checkMana(team_adding)}/{mana}]\n')
		showList(team_adding)
		print("[S]ave\t\t[C]lear\t\t[M]ana\t\t[Q]uit edit team\n")
		print("Invalid syntax! Try again.")
		select = input('Select: ').upper()
		if (select.isdigit()):
			if(int(select) <= 0 or int(select) > 95):
				select = ''
	if (select == 'S'):
		os.system('cls')
		if (len(team_adding) == 0):
			print('Team is empty! Try again.')
			select = ''
			time.sleep(1)
		else:
			print('Saved')
			'''
			notifi = input('Do you want continue? [Y/N] ').upper()
			while (notifi != 'Y' and notifi != 'N'):
				os.system('cls')
				notifi = input('Do you want continue? [Y/N]').upper()
			os.system('cls')
			if (notifi == 'N'):
				return 'Q'
			else:
				mana = inputMana()
			'''
			time.sleep(1)
	return select


def showListName():
	n = 1
	print('\tCard Name\tMana\n')
	for i in list_name:
		mn = card[i]['mana']
		if n < 10:
			print(f'{n:>2}. {i:<20} {mn}')
		else:
			print(f'{n}{".":<2}{i:<20} {mn}')
		n += 1



def addTeam():
	with open(team_path) as json_file:
		team = json.load(json_file)
	team_adding = []
	
	global mana
	mana = inputMana()

	select=''
	while (select != 'Q'):
		os.system('cls')
		showListName()
		print("\n")
		print(f'Mana: [{checkMana(team_adding)}/{mana}]\n')
		showList(team_adding)
		print("[S]ave\t\t[C]lear\t\t[M]ana\t\t[Q]uit edit team\n")
		select = menuOpt(input('Select: '), team_adding)

		
		if (select.isdigit()):
			team_adding.append(list_name[int(select)-1])

		#Save
		elif (select == 'S'):
			c = team.get(mana, 0)
			if (c != 0):
				team[mana].append(team_adding)
			else:
				team[mana] = []
				team[mana].append(team_adding)
			with open(team_path, 'w') as file:
				d = json.dump(team, file, indent=4)
			team_adding.clear()
		

		elif (select == 'C'):
			team_adding.clear()

		
		elif (select == 'M'):
			os.system('cls')
			mana = inputMana()
		
		print(team_adding)
	return select
	

def viewTeam():
	with open(team_path) as json_file:
		team = json.load(json_file)
	for i in team:
		print(f'Mana: {i}')
		for j in team[i]:
			print(j)
		print("\n")

	n = input('[Q]uit?\nSelect: ').upper()
	return n


def showList(list):
	if (len(list) > 0):
		print('-'*20)
		for i in range(len(list)):
			print(f'{i+1}. {list[i]} ')
		print('-'*20)


def ranTeam(Team1, Team2):
	a = random.randint(1,2)
	if (a==1):
		return Team1
	else:
		return Team2

def pickTeam(x):
	with open(team_path) as json_file:
		team = json.load(json_file)
	switcher={
		12: ranTeam(team['12'][0], team['12'][1]),
		13: team['13'],
		14: team['14'],
		15: team['15'],
		16: ranTeam(team['16'][0], team['16'][1]),
		17: ranTeam(team['17'][0], team['17'][1]),
		18: ranTeam(team['18'][0], team['18'][1]),
		19: team['19'],
		21: team['21'],
		22: team['22'],
		26: team['26']
	}
	return switcher.get(x, "No team")


def createCard():
	with open(src_web_path, mode="r", encoding="utf-8") as fp:
		soup = BeautifulSoup(fp, 'html.parser')


	name = soup.find_all(class_="card-name-name")
	level = soup.find_all(class_="card-name-level")
	mana = soup.find_all(class_="stat-text-mana")


	card = {}
	for i in range(95):
		lv = level[i].text
		card[name[i].text] = {"level": int(lv[2]), "mana": int(mana[i].text)}
	with open(card_path, 'w') as file:
		b = json.dump(card, file, indent=4)



logo = '''
					░██████╗██████╗░██╗░░░░░██╗██████╗░
					██╔════╝██╔══██╗██║░░░░░██║██╔══██╗
					╚█████╗░██████╔╝██║░░░░░██║██████╦╝
					░╚═══██╗██╔═══╝░██║░░░░░██║██╔══██╗
					██████╔╝██║░░░░░███████╗██║██████╦╝
					╚═════╝░╚═╝░░░░░╚══════╝╚═╝╚═════╝░
'''

def menu():
	os.system('cls')
	#print('\t****TEAM MANAGE****')
	print(logo)
	print(f"\t\t\t\t\t\t    Version {version}")
	print('\n1. START GAME\n2. Add team\n3. View team\n\n[Q]uit')
	select = input('\nSelect: ')
	if (select.isalpha()):
		select = select.upper()
	while (select!='1' and select!='2' and select!='3' and select!='Q'):
		os.system('cls')
		#print('\t****TEAM MANAGE****')
		print(logo)
		print(f"\t\t\t\t\t\t    Version {version}")
		print('\n1. START GAME\n2. Add team\n3. View team\n\n[Q]uit')
		print("Invalid syntax! Try again.")
		select = input('\nSelect: ')
		if (select.isalpha()):
				select = select.upper()
	return select

def shutDown():
	for i in range(3,0,-1):
		os.system('cls')
		print(f'Not working! Shut down in {i}')
		time.sleep(1)


def update():
	response = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/main/splib.py')
	f = io.open('splib.py', mode="w", encoding="utf-8")
	f.write(response.text)
	f.close()

def check_update():
	global version
	print('Checking update...')
	response = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/main/version')
	new_version = response.text[:3]
	if(version != new_version):
		os.system('cls')
		cf = input(f'New Update! Version {new_version}\nDo you want update? [Y/N] ')
		if (cf.isalpha()):
			cf = cf.upper()
		while(cf != 'Y' and cf != 'N'):
			os.system('cls')
			print("Invalid syntax! Try again.")
			cf = input('New Update! Do you want update? [Y/N] ')
			if (cf.isalpha()):
				cf = cf.upper()
		if (cf == 'Y'):
			update()
		version = new_version


def _main():
	check_update()
	select = menu()	
	while (select != 'Q'):
		os.system('cls')
		if (select == '1'):
			shutDown()
			select = menu()
		elif (select == '2'):
			n = addTeam()
			if (n == 'Q'):
				select = menu()
		elif (select == '3'):
			n = viewTeam()
			if (n == 'Q'):
				select = menu()
