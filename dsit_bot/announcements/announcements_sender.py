from dataclasses import dataclass

import requests
import logging

from dsit_bot.settings import bot_settings, update_announcements_config, initialize_bot_settings


@dataclass
class Announcement:
    title: str
    date: str
    link: str
    origin: str


def create_announcements_response(announcements, limit=5):
    """
    Create the text to send back to discord chat.
    Args:
        announcements: A list of Announcements objects
        limit: Limit of the announcements that will be printed
    Returns:
        The text of the response.
    """
    response_string = ""
    if announcements is not None:
        for ind, announcement in enumerate(announcements[:limit]):
            response_string += f"{ind}.\t**{announcement.title}** - *{announcement.date}*\n"
            # Using <, > around the link to disable auto-embed
            response_string += f"\t\tLink: <{announcement.link}>\n"
            response_string += "\n"
    else:
        response_string += "```diff\n" \
                           "- Failed to reach the DSIT announcements page.\n" \
                           "```"

    return response_string


def alert_new_announcement_response(new_announcement):
    if new_announcement.origin == 'DIT':
        new_announcement.origin = 'UoA-DIT'
    response_text = f"```css\n" \
                    f"New Announcement from {new_announcement.origin}!\n" \
                    "```\n" \
                    f"->\t**{new_announcement.title}** - *{new_announcement.date}*\n" \
                    f"\t\tLink: <{new_announcement.link}>\n\n"

    return response_text


def new_announcements_check(parse_announcements_method, origin, announcements):
    returned_announcements = update_announcements(bot_settings['announcements'][f'url_{origin}'],
                                                  parse_announcements_method, origin)

    if returned_announcements is not None:
        # new_ann True, means that the latest announcements of announcements list is new, send message to #general
        logging.info(f'Updated announcements of {origin} | Found new announcement')
        announcements[:] = returned_announcements
        return alert_new_announcement_response(announcements[0])
    else:
        logging.info(f'Updated announcements of {origin} | No new announcement')
        return None


def update_announcements(url, parse_announcements, origin):
    """
    Updates the announcements and returns if there was a new update
    Args:
        url: The url of the announcements homepage (currently DSIT or DIT)
        parse_announcements: A method that parses the announcements depending on the origin (DIT, DSIT)
        origin: DIT or DSIT

    Returns:
        List[Announcement] or None: If there were no new announcements we return None
    """
    try:
        new_announcements = parse_announcements(url)
    except requests.exceptions.RequestException:
        logging.warning('Failed to update announcements')
        return False

    # Can be removed, used for debugging purposes. It allows us to manually change the config files
    initialize_bot_settings()

    old_title = bot_settings['announcements'][f'last_{origin}_announcement']
    new_title = new_announcements[0].title

    if old_title == new_title:
        return None
    else:
        bot_settings['announcements'][f'last_{origin}_announcement'] = new_title
        update_announcements_config()
        return new_announcements
