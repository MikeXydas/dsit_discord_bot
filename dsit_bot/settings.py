"""
We load all the settings from the config files to a global dictionary (not the best design pattern).
Currently, the setting are loaded in memory when the bot is booting up.
"""

import json

bot_settings = {}


def initialize_bot_settings():
    # Reading the token (DO NOT INCLUDE IT IN THE REPO) and the general chat id
    try:
        with open('dsit_bot/config/bot_config.json', "r") as config_file:
            bot_config = json.load(config_file)
            bot_settings['token'] = bot_config['token']
            bot_settings['general_chat_id'] = bot_config['general_chat_id']
    except FileNotFoundError as e:
        raise Exception('Bot Configuration file not found - Run setup.py first from project root directory') from e

    # Initialize the announcement settings
    with open('dsit_bot/config/announcements_config.json') as json_file:
        bot_settings['announcements'] = json.load(json_file)


def update_announcements_config():
    with open('dsit_bot/config/announcements_config.json', 'w') as outfile:
        json.dump(bot_settings['announcements'], outfile)
