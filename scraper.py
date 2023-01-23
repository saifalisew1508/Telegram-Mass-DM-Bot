from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv

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
    all_participants = client.get_participants(target_group)
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
    print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time. OR try again with a smaller group.")
