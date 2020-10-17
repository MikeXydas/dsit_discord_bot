import logging
import requests

from discord.ext import commands

from .announcements import parse_dsit_announcements, create_announcements_response


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

    @client.command(aliases=['announcements'])
    async def send_announcements(ctx, limit=5):
        """
        Can be called using "!announcements 3" to send the 3 latest announcements of the DSIT page.

        Args:
            ctx: Discord context
            limit: Limit of the announcements that will be printed
        """
        await ctx.send(create_announcements_response(announcements, limit))

    client.run('NzY2OTI2NjYwODEyOTMxMTAy.X4qeHA.T7buaU3sqPwixfpmKCVekR0rQU4')