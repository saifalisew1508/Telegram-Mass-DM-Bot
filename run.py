from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import sys,os
import csv
import random
import time

auth = {}
with open('user_auth.csv', encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        auth = {}
        auth['api_id'] = int(row[0])
        auth['api_hash'] = row[1]
        auth['phone'] = row[2]

api_id = auth['api_id']
api_hash = auth['api_hash']
phone = auth['phone']
client = TelegramClient("anon",api_id, api_hash)
client.start(phone)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))


os.system('clear')


def scraper():
    chats = []
    last_date = None
    chunk_size = 100
    groups=[]

    result = client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=500,
            hash = 0
        ))


    chats.extend(result.chats)
    for chat in chats:
        try:
            if chat.megagroup== True:
                groups.append(chat)
        except:
            continue

    print('Choose a group to scrape members from:')
    i=0
    for g in groups:
        print(str(i) + '- ' + g.title)
        i+=1

    g_index = input("Enter a Number: ")
    target_group=groups[int(g_index)]

    print('Fetching Members...')
    all_participants = []
    try:
        all_participants = client.iter_participants(target_group)
        print('Saving In file...')
        with open("members.csv","w",encoding='UTF-8') as f:
            writer = csv.writer(f,delimiter=",",lineterminator="\n")
            writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
            for user in all_participants:
                if user.username:
                    username= user.username
                else:
                    username= ""
                if user.first_name:
                    first_name= user.first_name
                else:
                    first_name= ""
                if user.last_name:
                    last_name= user.last_name
                else:
                    last_name= ""
                name= (first_name + ' ' + last_name).strip()
                writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])      
        print('Members scraped successfully.')
    except TypeError:
        print("GOT THE FIRST 6000 MEMBERS OF THE GROUP")
    
def massMessager():
    SLEEP_TIME = int(input("Enter Delay Timing For Per Message Sending : "))

    input_file = "members.csv"
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

    mode = int(input("Enter 1 to send by user ID or 2 to send by username: "))
    # mode = 1
    
    messages= ""
    with open('message.txt') as f:
        messages = messages
        messages = "".join(f.readlines())


    for user in users:
        if mode == 2:
            if user['username'] == "":
                continue
            receiver = client.get_input_entity(user['username'])
        elif mode == 1:
            receiver = InputPeerUser(user['id'],user['access_hash'])
        else:
            print("Invalid Mode. Exiting.")
            client.disconnect()
            sys.exit()
        message = messages
        try:
            print("Sending Message to:", user['name'])
            client.send_message(receiver, message.format(user['name']))
            print("Waiting {} seconds".format(SLEEP_TIME))
            time.sleep(SLEEP_TIME)
        except PeerFloodError:
            print("Getting Flood Error from telegram.")
            print("waiting for 30secs and then trying to continue")
            time.sleep(30)
            continue
        except Exception as e:
            print("Error:", e)
            print("Trying to continue...")
            continue
    client.disconnect()
    print("Done. Message sent to all users.")



print("0 - Extract members from a group. \n1 - Send message to already extracted members. \n2 - Extract members from a group and send them the message.")
userChoice = int(input("Enter one of the opetions for what you want to do:"))

if userChoice == 0:
    scraper()
elif userChoice == 1:
    massMessager()
elif userChoice == 2:
    scraper()
    massMessager()
else:
    print("OPTION ENTERED BY YOU IS INVALID.")
