import os,sys
import csv
print("THIS IS SETUP FOR TELEGRAM BOT.")

api_id = input("PLEASE ENTER YOUR API ID: ")
os.system('clear')

api_hash = input("PLEASE ENTER YOUR API HASH: ")
os.system('clear')

phone = input("PLEASE ENTER YOUR PHONE NUMBER: ")
os.system('clear')

with open("user_auth.csv","w",encoding='UTF-8') as f:
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['api_id','api_hash','phone'])
        api_id = api_id
        api_hash = api_hash
        phone = phone

        writer.writerow([api_id,api_hash,phone])

print("AUTHENTICATION INFO SAVED TO FILE")