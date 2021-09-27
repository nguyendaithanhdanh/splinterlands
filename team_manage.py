import os, requests, io, time

def saveFile(filePath, content):
    f = io.open(filePath, mode="w", encoding="utf-8")
    f.write(content)
    f.close()

def d_src():
    response = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/main/splib.py')
    if response:
        saveFile('splib.py', response.text)
        from splib import main
        main()
    else:
        print("Please connect to internet!")
        for i in range(3):
            print(f"Shut down in {i+1}")
            time.sleep(1)
            os.system('cls')




if __name__ == "__main__":
    d_src()
