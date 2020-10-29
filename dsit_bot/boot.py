import logging
import requests

from discord.ext import commands, tasks

from .announcements import create_announcements_response, update_announcements, \
    alert_new_announcement_response, initialize_announcements
from .settings import bot_settings, initialize_bot_settings


# Logger settings
logging.basicConfig(level=logging.INFO, format='%(levelname)s | %(asctime)s | %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S')


def boot_up():
    # The command prefix will be used to invoke the bot from discord chat
    client = commands.Bot(command_prefix='!')

    # Read the settings of the bot from the config files
    initialize_bot_settings()

    # Read current DSIT announcements
    announcements = initialize_announcements()

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
        new_ann = update_announcements(bot_settings['announcements']['url'], announcements)
        if new_ann:
            # new_ann True, means that the latest announcements of announcements list is new, send message to #general
            logging.info('Updated announcements | Found new announcement')
            await channel.send(alert_new_announcement_response(announcements[0]))
        else:
            logging.info('Updated announcements | No new announcement')

    client.run(bot_settings['token'])
