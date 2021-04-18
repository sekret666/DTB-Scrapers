#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import configparser
import os, sys
import csv
import random
import time

re="\e[1;34m" #mavi
gr="\e[1;31m" #qirmizi
cy="\e[1;33m" #yasil
SLEEP_TIME = 30

class main():

    def banner():
        
        print(f"""

   _____   _______ ______        _                                       
  (____ \ (_______|____  \      | |                                      
   _   \ \ _       ____)  )      \ \   ____  ____ ____ ____   ____  ____ 
  | |   | | |     |  __  (        \ \ / ___)/ ___) _  |  _ \ / _  )/ ___)
  | |__/ /| |_____| |__)  )   _____) | (___| |  ( ( | | | | ( (/ /| |    
  |_____/  \______)______/   (______/ \____)_|   \_||_| ||_/ \____)_|    
                                                      |_|                

            """)

    def send_sms():
        try:
            cpass = configparser.RawConfigParser()
            cpass.read('config.data')
            api_id = cpass['cred']['id']
            api_hash = cpass['cred']['hash']
            phone = cpass['cred']['phone']
        except KeyError:
            os.system('clear')
            main.banner()
            print(re+"[!] run python3 setup.py first !!\n")
            sys.exit(1)

        client = TelegramClient(phone, api_id, api_hash)
         
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone)
            os.system('clear')
            main.banner()
            client.sign_in(phone, input(gr+'[+] Enter the code: '+re))
        
        os.system('clear')
        main.banner()
        input_file = sys.argv[1]
        users = []
        with open(input_file, encoding='UTF-8') as f:
            rows = csv.reader(f,delimiter=",",lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                users.append(user)
        print(yasil+"[1] send sms by user ID\n[2] send sms by username ")
        mode = int(input(yasil+"Input : "+re))
         
        message = input(yasil+"[+] Enter Your Message : "+re)
         
        for user in users:
            if mode == 2:
                if user['username'] == "":
                    continue
                receiver = client.get_input_entity(user['username'])
            elif mode == 1:
                receiver = InputPeerUser(user['id'],user['access_hash'])
            else:
                print(qirmizi+"[!] Invalid Mode. Exiting.")
                client.disconnect()
                sys.exit()
            try:
                print(yasil+"[+] Sending Message to:", user['name'])
                client.send_message(receiver, message.format(user['name']))
                print(yasil+"[+] Waiting {} seconds".format(SLEEP_TIME))
                time.sleep(SLEEP_TIME)
            except PeerFloodError:
                print(yasil+"[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
                client.disconnect()
                sys.exit()
            except Exception as e:
                print(qirmizi+"[!] Error:", e)
                print(qirmizi+"[!] Trying to continue...")
                continue
        client.disconnect()
        print("Done. Message sent to all users.")



main.send_sms()
