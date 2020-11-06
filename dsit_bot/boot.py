import logging

from discord.ext import commands, tasks

from dsit_bot.announcements.announcements_sender import create_announcements_response, new_announcements_check
from dsit_bot.announcements.dsit_announcements import initialize_dsit_announcements, parse_dsit_announcements
from dsit_bot.announcements.uoa_dit_announcements import initialize_uoa_dit_announcements, parse_dit_uoa_announcements

from .settings import bot_settings, initialize_bot_settings

# Logger settings
logging.basicConfig(level=logging.INFO, format='%(levelname)s | %(asctime)s | %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S')


def boot_up():
    # The command prefix will be used to invoke the bot from discord chat
    client = commands.Bot(command_prefix='!')

    # CARE: This must be the id of the channel we want to send the update and is different from server to server
    # In order for the channel id to be visible you must enable Discord's developer mode.
    general_channel_id = 766929768753922051

    # Read the settings of the bot from the config files
    initialize_bot_settings()

    # Read current DSIT announcements
    dsit_announcements = initialize_dsit_announcements()
    dit_uoa_announcements = initialize_uoa_dit_announcements()

    @client.event
    async def on_ready():
        logging.info("Bot is ready!")
        task_update_dsit_announcements.start()
        task_update_dit_uoa_announcements.start()

    @client.command(aliases=['announcements'])
    async def send_dsit_announcements(ctx, limit=5):
        """
        Can be called using "!announcements 3" to send the 3 latest announcements of the DSIT page.

        Args:
            ctx: Discord context
            limit: Limit of the announcements that will be printed
        """
        await ctx.send(create_announcements_response(dsit_announcements, limit))

    @tasks.loop(seconds=10)
    async def task_update_dsit_announcements():
        alert_msg = new_announcements_check(parse_dsit_announcements, 'DSIT', dsit_announcements)
        if alert_msg is not None:
            await client.get_channel(general_channel_id).send(alert_msg)

    @tasks.loop(seconds=10)
    async def task_update_dit_uoa_announcements():
        alert_msg = new_announcements_check(parse_dit_uoa_announcements, 'DIT', dit_uoa_announcements)
        if alert_msg is not None:
            await client.get_channel(general_channel_id).send(alert_msg)

    # Initialization completed, run the bot
    client.run(bot_settings['token'])
