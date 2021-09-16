from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from bs4 import BeautifulSoup
import getpass, time, io, json, random, os, requests, update, re


version = '1.5'
username = getpass.getuser()
usr_path=('C:/Users/', username, '/AppData/Local/Google/Chrome/User Data')
filePath = ''.join(usr_path)

card_path = './data/card.json'
team_path = './data/team.json'
src_web_path = './data/source_web.html'
color_path = './data/color_card.json'
acc_path = './data/account.json'
his_path = './data/history.json'



with open(card_path) as json_file:
    card = json.load(json_file)
list_card_name = []
for i in card:
    list_card_name.append(i)
list_name = sorted(list_card_name)
mana = 0

def add_account():
    try:
        with open(acc_path) as json_file:
            all_acc = json.load(json_file)
    except Exception as e:
        all_acc = [] 
    acc = {}
    os.system('cls')

    mail = input('Email: ')
    pwd = input('Password: ')

    acc['mail'] = mail
    acc['pwd'] = pwd
    #print(acc)
    #input()
    all_acc.append(acc)
    with open(acc_path, 'w') as file:
        d = json.dump(all_acc, file, indent=4)



def tme():
    with open(team_path) as json_file:
        team = json.load(json_file)
    return team

def getProf_Firefox():
    username = getpass.getuser()
    a = os.listdir('C:/Users/' + username + '/AppData/Roaming/Mozilla/Firefox/Profiles')
    prof_name = ''
    for i in a:
        if len(i) > 16:
            if i[-16:] == '.default-release':
                prof_name = i
    prof_path = 'C:/Users/' + username + '/AppData/Roaming/Mozilla/Firefox/Profiles/' + prof_name
    return prof_path

def pickranTeam(mana, card_path):
    with open(color_path) as json_file:
        color = json.load(json_file)
    count_mana = 0
    lst_color = list(color.keys())
    list_name = []
    p = random.randint(0,2)
    # Return color
    g_color = lst_color[p]
    while(int(count_mana) <= int(mana) and len(list_name) <= 7):
        macrr = count_mana
        r = random.randrange(0, len(color[g_color]))
        name = color[g_color][r]
        list_name.append(name)
        count_mana += int(card[name]['mana'])
    return list_name

def status(stt):
    os.system('cls')
    print(stt)


def writeHistory(driver, his_path, times):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rlt_soup = soup.find_all(class_="battle-log-entry")
    for n in range(times):
        try:
            with open(his_path) as json_file:
                history = json.load(json_file)
                json_file.close()
        except Exception as e:
            history = {}
        btl_log=re.compile(r'\d+|\w+\s?\w*\s?\w*\s?\w*[^(\n)]').findall(rlt_soup[n].text)
        me = []
        enemy = []
        for i in range(3,len(btl_log)):
            if btl_log[i] !='VS':
                me.append(btl_log[i])
            else:
                break
        en_name = ''
        en_rat = ''
        en_gui = ''

        for j in range(len(btl_log)-3, -1, -1):
            if btl_log[j].isdigit():
                en_name = btl_log[j+1]
                en_rat = btl_log[j]
                en_gui = btl_log[j+2]
                for z in range(j+3, len(btl_log)-3):
                    enemy.append(btl_log[z])
                break

        result = btl_log[len(me)+4]
        mode = btl_log[-3]
        mana=btl_log[len(me)+7]
        if mana == '0':
            mana=btl_log[len(me)+9]
        if mana == 'DEC':
            mana=btl_log[len(me)+10]
            
        my_team = {}
        my_team['name'] = btl_log[1]
        my_team['rating'] = btl_log[0]
        my_team['guid_name'] = btl_log[2]
        my_team['team'] = me

        enemy_team = {}
        enemy_team['name'] = en_name
        enemy_team['rating'] = en_rat
        enemy_team['guid_name'] = en_gui
        enemy_team['team'] = enemy


        result_ = result[:-3]
        if result[:-3] != "Battle Lost" and result[:-3] != "Battle Won":
            result_ = 'Draw'

        match = {}
        match['mode'] = mode[:-4]
        match['result'] = result_
        match['my_team'] = my_team
        match['enemy_team'] = enemy_team

        if history.get(mana, 'Non') == 'Non':
            history[mana] = []
            history[mana].append(match)
        else:
            history[mana].append(match)
        with open(his_path, 'w') as file:
            d = json.dump(history, file, indent=4)
            file.close()


def listToString(lst):
    strlst = "['"
    strlst += "', '".join(lst)
    strlst += "']"
    return strlst


def battle(match):
    
    '''
    with open(acc_path) as json_file:
        all_acc = json.load(json_file)
    for i in range(len(all_acc)):
        print(f'{i+1}. {all_acc[i]["mail"]}')
    sl = int(input('Select account: '))
    acc = all_acc[sl-1]
    '''
    

    status('Opening browser...')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-data-dir="+filePath)
    driver = webdriver.Chrome('./data/webdriver/chromedriver', options = chrome_options)
    wait = WebDriverWait(driver, 500)
    driver.get('https://splinterlands.com/?p=battle_history')
    try:
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div/div[1]/div[1]")))
        driver.execute_script("document.getElementsByClassName('modal-close-new')[0].click();")
    except Exception as e:
        pass
    
    '''
    driver.find_element_by_id('log_in_button').click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-body")))
    time.sleep(1)
    driver.find_element_by_id('email').send_keys(acc['mail'])
    driver.find_element_by_id('password').send_keys(acc['pwd'])
    driver.find_element_by_css_selector('form.form-horizontal:nth-child(2) > div:nth-child(3) > div:nth-child(1) > button:nth-child(1)').click()
    '''
    

    check_point = 0
    clone_i = 0
    for i in range(int(match)):
        clone_i = i+1
        wait.until(EC.visibility_of_element_located((By.ID, "battle_category_btn")))
        vf = i+1
        if vf % 20 == 0:
            time.sleep(5)
            writeHistory(driver, his_path, 20)
            check_point = vf
        driver.execute_script("var roww = document.getElementsByClassName('row')[1].innerHTML;var reg = /HOW TO PLAY|PRACTICE|CHALLENGE|RANKED/;var resultt = roww.match(reg);while(resultt != 'RANKED'){document.getElementsByClassName('slider_btn')[1].click();roww = document.getElementsByClassName('row')[1].innerHTML;resultt = roww.match(reg);};")
        time.sleep(1)
        status('Seeking Enemy...')
        driver.execute_script("document.getElementsByClassName('big_category_btn red')[0].click();")
        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div/div[2]/div[3]/div[2]/button")))
        time.sleep(1.5)
        mana = driver.find_element_by_css_selector('div.col-md-3:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)').text
        team = pickTeam(mana)
        if team == 'None':
            team = pickranTeam(mana, card)
        
        status('Creating team...')
        driver.execute_script("document.getElementsByClassName('btn btn--create-team')[0].click();")
        #Select card
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="page_container"]/div/div[1]/div')))
        status('Picking card...')
        tm = listToString(team)
        time.sleep(7)
        try:
            driver.execute_script("var team = "+ tm + ";for (let i = 0; i < team.length; i++) {let card = document.getElementsByClassName('card beta');let cimg = document.getElementsByClassName('card-img');var reg = /[A-Z]\\w+( \\w+'*\\w*)*/;for (let j = 0; j < card.length; j++){let att_card = card[j].innerText;let result = att_card.match(reg);let name = result[0];if (name == team[i]){cimg[j].click();break;}}}document.getElementsByClassName('btn-green')[0].click();")
        except Exception as e:
            time.sleep(3)
            driver.execute_script("var team = "+ tm + ";for (let i = 0; i < team.length; i++) {let card = document.getElementsByClassName('card beta');let cimg = document.getElementsByClassName('card-img');var reg = /[A-Z]\\w+( \\w+'*\\w*)*/;for (let j = 0; j < card.length; j++){let att_card = card[j].innerText;let result = att_card.match(reg);let name = result[0];if (name == team[i]){cimg[j].click();break;}}}document.getElementsByClassName('btn-green')[0].click();")            
        try:
            status('Waiting...')
            WebDriverWait(driver, 150).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#btnRumble')))
            driver.execute_script("document.getElementsByClassName('btn-battle')[0].click()")
            status('Rumbling...')
            time.sleep(3.5)
            status('Skiping')
            #wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#btnSkip')))
            driver.execute_script("document.getElementsByClassName('btn-battle')[1].click()")
        except Exception as e:
            status('Done')
            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dialog_container"]/div/div/div/div[1]/h1')))
            driver.execute_script("document.getElementsByClassName('btn btn--done')[0].click();")

        
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dialog_container"]/div/div/div/div[1]/h1')))
        driver.execute_script("document.getElementsByClassName('btn btn--done')[0].click();")
        status('Done')
    time.sleep(5)
    times_when_smaller_20 = clone_i - check_point
    if times_when_smaller_20 > 0:
        writeHistory(driver, his_path, times_when_smaller_20)
    driver.quit()
    return 'Q'





def checkMana(add):
    mana = 0
    for i in add:
        mana += card[i]['mana']
    return mana

def saveFile(filePath, content):
    f = io.open(filePath, mode="w", encoding="utf-8")
    f.write(content)
    f.close()


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
    list_options = ['S', 'C', 'Q', 'M', 'D']
    while (not btn(select, list_options) and (not select.isdigit())):
        os.system('cls')
        showListName()
        print("\n")
        print(f'Mana: [{checkMana(team_adding)}/{mana}]\n')
        showList(team_adding)
        print("[S]ave\t\t[C]lear All\t\t[M]ana\t\t[D]elete\t\t[Q]uit edit team\n")
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
            os.system('cls')
            print('Team have been saved!')
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
    n = 0
    a = []
    num = []
    for i in range(30, len(list_name), 30):
        b = []
        l = []
        for j in range(n, i):
            b.append(list_name[j])
            l.append(str(j+1))
        a.append(b)
        num.append(l)
        n = i
    c = []
    m = []
    for i in range(n, len(list_name)):
        c.append(list_name[i])
        m.append(str(i+1))
    if len(c) !=30:
        for i in range(len(c), 30):
            c.append('')
            m.append('')
    a.append(c)
    num.append(m)
    for i in range(30):
        print(f'{num[0][i]:>2} {a[0][i]:<25} {num[1][i]:>2} {a[1][i]:<25} {num[2][i]:>2} {a[2][i]:<25} {num[3][i]:>2} {a[3][i]:<25}')

def teamSorted(team):
    s = team.keys()
    s_int = []
    for i in s:
        s_int.append(int(i))
    s_sorted = sorted(s_int)

    team_sorted = {}
    for i in s_sorted:
        p = team.get(str(i))
        team_sorted[i] = p
    return team_sorted


def addTeam():

    team_adding = []
    
    global mana
    mana = inputMana()

    select=''
    while (select != 'Q'):
        with open(team_path) as file:
            team = json.load(file)
        os.system('cls')
        showListName()
        print("\n")
        print(f'Mana: [{checkMana(team_adding)}/{mana}]\n')
        showList(team_adding)
        print("[S]ave\t\t[C]lear All\t\t[M]ana\t\t[D]elete\t\t[Q]uit edit team\n")
        select = menuOpt(input('Select: '), team_adding)

        
        if (select.isdigit()):
            team_adding.append(list_name[int(select)-1])
 
        #Save
        elif (select == 'S'):
            c = team.get(str(mana), 'NotFound')
            if (c != 'NotFound'):
                team[str(mana)].append(team_adding)
            else:
                team[str(mana)] = []
                team[str(mana)].append(team_adding)
            
            team_sorted = teamSorted(team)

            with open(team_path, 'w') as file:
                d = json.dump(team_sorted, file, indent=4)
            team_adding.clear()
        elif (select == 'C'):
            team_adding.clear()
        elif (select == 'M'):
            os.system('cls')
            mana = inputMana()
        elif (select == 'D'):
            team_adding.pop(-1)
        print(team_adding)
    return select

def list_name_dict():
    lname = {}
    for i in range(1, len(list_name)+1):
        lname[list_name[i-1]] = str(i)
    return lname 


def kpi(his_path, mana, team):
    with open(his_path) as json_file:
        history = json.load(json_file)
    won = 0
    lost = 0
    drawn = 0
    match = 0
    if history.get(mana, 'None') != 'None':
        for i in range(len(history[mana])):
            if history[mana][i]['my_team']['team'] == team:
                if history[mana][i]['result'] == 'Battle Won':
                    won += 1
                if history[mana][i]['result'] == 'Battle Lost':
                    lost += 1
                if history[mana][i]['result'] == 'Drawn':
                    drawn += 1
        match = won + lost + drawn
    return [won, lost, drawn, match]


def analys(his_path, team_path):
    with open(his_path) as json_file:
        history = json.load(json_file)
    with open(team_path) as json_file:
        team = json.load(json_file)
    print('\n[Q]uit\n')
    mana = input('Enter mana to view details: ').upper()
    while((team.get(mana, 'Non') == 'Non') and mana != 'Q'):
        print('[!] Mana is not available!')
        time.sleep(1)
        os.system('cls')
        viewTeam()
        print('\n[Q]uit\n')
        mana = input('Enter mana to view details: ').upper()
    if mana == 'Q':
        return 'Q'
    else:
        os.system('cls')
        print(f' Mana {mana}:\n')
        j = 1
        for i in team[mana]:
             print(f'{j}. {i}')
             j += 1
        te = int(input('Select team: '))
        te -=1
        b = team[mana][te]

        kp = kpi(his_path, mana, b)

        os.system('cls')
        print(f'Team: {b}')
        print(f"\nIn {kp[3]} match:")
        print(f'    Won: {kp[0]}')
        print(f'    Lost: {kp[1]}')
        print(f'    Drawn: {kp[2]}')
        
        if kp[3] != 0:
            print('\n\t\t\t\t\t\tHISTORY ENEMY TEAM\n')
            for i in range(len(history[mana])):
                if history[mana][i]['my_team']['team'] == b:
                    rsl = history[mana][i]['result']
                    x = rsl[7:]
                    if x != 'Won' and x!='Lost':
                        x = "Drawn"
                    print(f'> {x:<4}', end=": ")
                    print('[', end="")
                    print(", ".join(history[mana][i]['enemy_team']['team']), end="")
                    print(']')
                    xx = []
                    pp = list_name_dict()
                    for k in history[mana][i]['enemy_team']['team']:
                        xx.append(pp.get(k))
                    num = " / ".join(xx)
                    print(f'Number [{num}]')
        n = input('\n[Q]uit\t[R]eturn View team\nSelect: ').upper()
        while(n!='R' and n!='Q'):
            os.system('cls')
            print('Invalid syntax!')
            n = input('\n[Q]uit\t[R]eturn View team\nSelect: ').upper()
        if n == 'R':
            return 'R'
        else:
            return 'Q'


def viewTeam():
    os.system('cls')
    with open(team_path) as json_file:
        team = json.load(json_file)
    for i in team:
        print('_'*120)
        print(f'\n MANA {i}:')
        k = 1
        for j in team[i]:
            kp = kpi(his_path, i, j)
            percent = 0.0
            if kp[3] != 0:
                percent = int(kp[0]) / int(kp[3]) *100
            p = ", ".join(j)
            print(f'{k}. {p}')
            print(f'   --> Won: {kp[0]}  /  Lost: {kp[1]}  /  Drawn: {kp[2]} | in {kp[3]} match | Win rate {percent}%')
            k += 1
        print()
    print('_'*120)
    print()


def showList(list):
    if (len(list) > 0):
        print('-'*20)
        for i in range(len(list)):
            print(f'{i+1}. {list[i]} ')
        print('-'*20)



def delTeamGUI():
    z = 'Q'
    while(z == 'Q'):
        with open(team_path) as json_file:
            list_team = json.load(json_file)
        os.system('cls')
        viewTeam()
        x = input('\nSelect a mana: ')
        lt = list_team.get(x, 'None')
        while lt == 'None':
            os.system('cls')
            viewTeam()
            print('\nTeam not found! Try again.')
            x = input('\nSelect a mana: ')
            print('\nSelect a team to delete:\n')
            lt = list_team.get(x, 'None')
        os.system('cls')
        print(f'Mana: {x}')
        print('\nSelect a team to delete:\n')
        for i in range(len(lt)):
            print(f'{i+1}. {lt[i]}')
        td = input('\nSelect: ')

        while((td <= '0' or td > str(len(lt))) and td.isalpha):
            os.system('cls')
            print(f'Mana: {x}')
            print('\nSelect a team to delete:\n')
            for i in range(len(lt)):
                print(f'{i+1}. {lt[i]}')
            print("\nInvalid syntax! Try again.")
            td = input('Select: ')

        os.system('cls')
        st = lt[int(td)-1]
        acpt = input(f'Team selected:\n{st}\n\nDo you want delete this team? [Y/N]\nSelect: ').upper()
        while (acpt != 'Y' and acpt != 'N'):
            os.system('cls')
            print("Invalid syntax! Try again.")
            acpt = input(f'Team selected:\n{st}\n\nDo you want delete this team? [Y/N]\nSelect: ').upper()
        if acpt == 'Y':
            list_team[x].pop(int(td)-1)
            if len(list_team[x]) == 0:
                list_team.pop(x)
            with open(team_path, 'w') as file:
                b = json.dump(list_team, file, indent=4)
            os.system('cls')
            print('Done')
            time.sleep(1)
            z = 'Q'
        else:
            z = 'Q'

def delTeam():
    with open(team_path) as json_file:
        list_team = json.load(json_file)
    os.system('cls')
    viewTeam()
    x = input('\nSelect a mana: ')
    lt = list_team.get(x, 'None')
    while lt == 'None':
        os.system('cls')
        viewTeam()
        print('\nTeam not found! Try again.')
        x = input('\nSelect a mana: ')
        print('\nSelect a team to delete:\n')
        lt = list_team.get(x, 'None')
    os.system('cls')
    print(f'Mana: {x}')
    print('\nSelect a team to delete:\n')
    for i in range(len(lt)):
        print(f'{i+1}. {lt[i]}')
    td = input('\nSelect: ')

    while((td <= '0' or td > str(len(lt))) and td.isalpha):
        os.system('cls')
        print(f'Mana: {x}')
        print('\nSelect a team to delete:\n')
        for i in range(len(lt)):
            print(f'{i+1}. {lt[i]}')
        print("\nInvalid syntax! Try again.")
        td = input('Select: ')

    os.system('cls')
    st = lt[int(td)-1]
    acpt = input(f'Team selected:\n{st}\n\nDo you want delete this team? [Y/N]\nSelect: ').upper()
    while (acpt != 'Y' and acpt != 'N'):
        os.system('cls')
        print("Invalid syntax! Try again.")
        acpt = input(f'Team selected:\n{st}\n\nDo you want delete this team? [Y/N]\nSelect: ').upper()
    if acpt == 'Y':
        list_team[x].pop(int(td)-1)
        if len(list_team[x]) == 0:
            list_team.pop(x)
        with open(team_path, 'w') as file:
            b = json.dump(list_team, file, indent=4)
        os.system('cls')
        print('Done')
        time.sleep(1)
        return 'Q'
    else:
        return 'Q'


def ranTeam(team):
    if len(team) == 1:
        return team[0]
    else:
        a = random.randrange(0,len(team))
        return team[a]

def pickTeam(x):
    with open(team_path) as json_file:
        team = json.load(json_file)
        t = team.get(str(x), "None")
    if t != 'None':
        return ranTeam(t)
    else:
        return t

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
\t\t\t\t\t░██████╗██████╗░██╗░░░░░██╗██████╗░
\t\t\t\t\t██╔════╝██╔══██╗██║░░░░░██║██╔══██╗
\t\t\t\t\t╚█████╗░██████╔╝██║░░░░░██║██████╦╝
\t\t\t\t\t░╚═══██╗██╔═══╝░██║░░░░░██║██╔══██╗
\t\t\t\t\t██████╔╝██║░░░░░███████╗██║██████╦╝
\t\t\t\t\t╚═════╝░╚═╝░░░░░╚══════╝╚═╝╚═════╝░
'''

def menu():
    os.system('cls')
    #print('\t****TEAM MANAGE****')
    print(logo)
    print(f"\t\t\t\t\t\t    Version {version}")
    print('\n1. START GAME\n2. Add team\n3. View team\n4. Delete team\n\n[Q]uit')
    select = input('\nSelect: ')
    if select.isalpha():
        select = select.upper()
    list_op = ['1', '2', '3','4', 'Q']
    while (not btn(select, list_op)):
        os.system('cls')
        #print('\t****TEAM MANAGE****')
        print(logo)
        print(f"\t\t\t\t\t\t    Version {version}")
        print('\n1. START GAME\n2. Add team\n3. View team\n4. Delete team\n\n[Q]uit')
        print("Invalid syntax! Try again.")
        select = input('\nSelect: ')
        if select.isalpha():
            select = select.upper()
    return select

def shutDown(mess):
    for i in range(3,0,-1):
        os.system('cls')
        print(mess)
        print(f'Shut down in {i}')
        time.sleep(1)

def getUpdate():
    response = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/main/update.py')
    saveFile('update.py', response.text)

def check_update():
    global version
    print('Checking Update...')
    response = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/main/version')
    new_version = response.text[:3]
    if(version != new_version):
        os.system('cls')
        cf = input(f'New Update! Version {new_version}\nDo you want Update? [Y/N] ')
        if (cf.isalpha()):
            cf = cf.upper()
        while(cf != 'Y' and cf != 'N'):
            os.system('cls')
            print("Invalid syntax! Try again.")
            cf = input('New update! Do you want update? [Y/N] ')
            if (cf.isalpha()):
                cf = cf.upper()
        if (cf == 'Y'):
            os.system('cls')
            print('Updating...')
            getUpdate()
            update.update_lib()
            os.system('cls')
            time.sleep(1)
            shutDown('Updated!')
            return 'OK'

def btn(x,li):

    if (x.isalpha()):
        x = x.upper()
    check = False
    for i in li:
        if x == i:
            check = True
            break   
    return check        

def _main():
    select = ''
    upd = check_update()
    if upd == 'OK':
        select = 'Q'
    else:
        select = menu()
    while (select != 'Q'):
        os.system('cls')
        if (select == '1'):
            match = input('Number of match: ')
            n = battle(match)
            if (n == 'Q'):
                select = menu()
        elif (select == '2'):
            n = addTeam()
            if (n == 'Q'):
                select = menu()
        elif (select == '3'):
            viewTeam()
            n = analys(his_path, team_path)
            #
            if (n == 'Q'):
                select = menu()
            elif (n== 'R'):
                select == '3'
        elif (select == '4'):
            n = delTeam()
            if (n == 'Q'):
                select = menu()
    os.system('cls')
