# MSc Discord Bot

A discord bot aiming to help us with tasks like notifying, providing info, sending us cat pics (pending), etc.

## Current Services

* Notifying in the general chat when a new announcement is posted in the DSIT page
* Presenting the last x announcements using the command `!announcements x`
  
I would be more than happy to send me ideas, issues and PRs  
  
## Setting Up

1. **Python Environment**
    1. The bot is developed with **Python3.8** so make sure you have it installed in your system
    2. The package manager I used was [poetry](https://python-poetry.org/). 
        Follow the [installation steps](https://python-poetry.org/docs/#installation) of your respective OS. 
        (Although not suggested, you can avoid using poetry and create an environment using `conda` or `venv`.)
    4. If you did not install poetry there is a `requirements.txt` file you can use to install
       the dependencies
2. **Creating a Discord Bot**  
    1. First create a discord server you will use to test the bot (name does not matter)
    2. Go to https://discord.com/developers/applications and press `New Application` (the name does not matter)
    3. From the left go to Bot > Add Bot > Yes
    4. Next to the icon there is a **Token**. When connecting to the bot this token will be used (more later).
    5. From the left go to OAuth2
    6. On scopes select `Bot`
    7. On bot permissions select `Administrator`
    8. Copy the link between scopes and permission and paste it in a browser. The bot 
       should now join your development server.
3. **Cloning and Running**
    1. ``git clone`` and `cd` in the repo
    2. **If you installed poetry** run `poetry install`
    3. (Not tested) **If you did not install poetry**, install the dependencies using `requirements.txt` (CARE: python version >=3.8)
    4. Create the empty file `dsit_bot/config/bot_token.tok` and paste in it the **Token** we mentioned above
    5. From the root directory of the project run `poetry run python3 main.py`
    6. To test if the bot is running got to your dev server and type in any chat `!announcements` expecting
       the last 5 announcements of DSIT to appear

**Note**: For the notification of a new announcement the bot requires a text channel ID that will
print the announcement. Currently, I have it hardcoded as the channel id of the #general in our server 
(dsit_bot/boot.py, line 50). This is bad and I should fix it.   
For now you should follow the steps below to fix it:
1. Go to Discord User Settings > Appearance > Enable Developer Mode
2. Go to you dev server > right click on #general > Copy Id
3. Paste it in the dsit_bot/boot.py, line 50 (currently the id you must change is 761925517661175812)

Feel free to tell me if there are any mistakes, needed clarifications or in general if you are having
trouble setting it up.


