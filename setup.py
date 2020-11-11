"""
A setup script creating the configuration file containing the SECRET bot token id and the #general chat id.
"""
import json

print(">>> DSIT Discord Bot Setup")

token = input('- Input the token of your development bot (check README.md for more info):\nToken: ')
general_chat_id = int(input('- Input the id of your #general chat that the announcements will be sent\nId: '))

config_file = {
    "token": token,
    "general_chat_id": general_chat_id
}

with open('dsit_bot/config/bot_config.json', 'w') as outfile:
    json.dump(config_file, outfile)

print(">>> Successfully finished setup")
