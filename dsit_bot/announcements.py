from dataclasses import dataclass
from bs4 import BeautifulSoup

import requests
import logging
import datetime
import json
import pytz

@dataclass
class Announcement:
    title: str
    date: str
    link: str


def parse_dsit_announcements(url):
    """
    Creates a list of Announcement objects parsed from the announcements page of the DSIT homepage.

    Args:
        url: The url of the announcements page, currently: http://dsit.di.uoa.gr/?page_id=28

    Returns:
        A list of Announcement objects

    Raises:
        requests.exceptions.RequestException: If we fail to connect to the DSIT announcement page
    """
    try:
        resp = requests.get(url)
        resp.raise_for_status()    # Raising request exception if status code is not 200
    except requests.exceptions.RequestException as e:
        logging.error('Failed to reach DSIT announcements page')
        raise e

    announce_soup = BeautifulSoup(resp.text, features="html.parser")
    articles = announce_soup.find_all('article')

    def parse_announcement(announcement):
        # Date parsing, converting to local timezone and casting again as string
        date_str = announcement.find('span', attrs={'class': 'updated'})
        date_time_obj = datetime.datetime.strptime(date_str.text, '%Y-%m-%dT%H:%M:%S%z')\
            .astimezone(tz=pytz.timezone('Europe/Athens'))

        # Dates are surprisingly not ordered since we extract the last update time and not posting time
        converted_datetime = date_time_obj.strftime("%d-%m-%Y %H:%M")

        # Announcement link parsing
        href = announcement.find_all('a')[1]['href']

        # Title Parsing
        title = announcement.find_all('a')[1].contents[0]

        return title, converted_datetime, href

    announcements = [Announcement(*parse_announcement(article)) for article in articles]

    return announcements


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


def update_announcements(url, old_announcements):
    """
    Updates the announcements and returns if there was a new update
    Args:
        url: The url of the DSIT announcements homepage
        old_announcements: A list of Announcement objects that will get updated

    Returns:
        Boolean, True if there was a new announcement or False if there was not
    """
    try:
        old_announcements[:] = parse_dsit_announcements(url)
    except requests.exceptions.RequestException:
        logging.warning('Failed to update announcements')
        return False

    ann_config = read_config()
    old_date = ann_config['last_announcement']
    new_date = old_announcements[0].date

    if old_date == new_date:
        return False
    else:
        ann_config['last_announcement'] = new_date
        update_config(ann_config)  # We must update the time of our new latest announcement
        return True


def alert_new_announcement_response(new_announcement):
    response_text = f"```css\n" \
                    "New Announcement from DSIT!\n" \
                    "```\n" \
                    f"->\t**{new_announcement.title}** - *{new_announcement.date}*\n" \
                    f"\t\tLink: <{new_announcement.link}>\n\n"

    return response_text


def read_config():
    with open('dsit_bot/config/announcements_config.json') as json_file:
        ann_config = json.load(json_file)
    return ann_config


def update_config(new_configs):
    with open('dsit_bot/config/announcements_config.json', 'w') as outfile:
        json.dump(new_configs, outfile)
