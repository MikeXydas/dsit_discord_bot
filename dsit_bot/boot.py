import logging
import requests

from discord.ext import commands, tasks

from .announcements import parse_dsit_announcements, create_announcements_response, update_announcements, \
    alert_new_announcement_response


def boot_up():
    # Logger settings
    logging.basicConfig(level=logging.INFO, format='%(levelname)s | %(asctime)s | %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S')

    # The command prefix will be used to invoke the bot from discord chat
    client = commands.Bot(command_prefix='!')

    # ## Load data like announcements, courses info, etc.  ##

    # Announcements loading
    announcements_url = 'http://dsit.di.uoa.gr/?page_id=28'
    announcements = None
    try:
        logging.debug('Requesting announcements from DSIT announcement page')
        announcements = parse_dsit_announcements(announcements_url)
        logging.debug('Successfully parsed DSIT announcements')
    except requests.exceptions.RequestException:
        logging.error(f'Could not reach DSIT announcement page using {announcements_url}')

    @client.event
    async def on_ready():
        logging.info("Bot is ready!")
        task_update_announcements.start()

    @client.command(aliases=['announcements'])
    async def send_announcements(ctx, limit=5):
        """
        Can be called using "!announcements 3" to send the 3 latest announcements of the DSIT page.

        Args:
            ctx: Discord context
            limit: Limit of the announcements that will be printed
        """
        await ctx.send(create_announcements_response(announcements, limit))

    @tasks.loop(minutes=10)
    async def task_update_announcements():
        # CARE: This must be the id of the channel we want to send the update and is different from server to server
        # In order for the channel id to be visible you must enable Discord's developer mode.
        channel = client.get_channel(766929768753922051)
        new_ann = update_announcements(announcements_url, announcements)
        if new_ann:
            logging.info('Updated announcements | Found new announcement')
            await channel.send(alert_new_announcement_response(announcements[0]))
        else:
            logging.info('Updated announcements | No new announcement')

    # Reading the token (DO NOT INCLUDE IT IN THE REPO) and running the bot
    with open('dsit_bot/config/bot_token.tok', "r") as token_file:
        bot_token = token_file.read()
    client.run(bot_token)
