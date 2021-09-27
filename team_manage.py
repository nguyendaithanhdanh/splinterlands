import os, requests, time

if __name__ == "__main__":
    response = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/main/splib.py')
    if response:
        with open('splib.py', mode="w", encoding="utf-8") as f:
            f.write(response.text)
            f.close()
        from splib import main
        main()
    else:
        print("Please connect to internet!")
        for i in range(3):
            print(f"Shut down in {i+1}")
            time.sleep(1)
            os.system('cls')
