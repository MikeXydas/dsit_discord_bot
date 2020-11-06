from bs4 import BeautifulSoup

import requests
import logging
import datetime
import pytz

from dsit_bot.settings import bot_settings
from dsit_bot.announcements.announcements_sender import Announcement


def initialize_dsit_announcements():
    """
    Initializes a list of announcements that are requested and parsed from the DSIT announcements page.

    Returns:
        A list of Announcement objects
    """
    announcements_url = bot_settings['announcements']['url_DSIT']
    announcements = None
    try:
        logging.debug('Requesting announcements from DSIT announcement page')
        announcements = parse_dsit_announcements(announcements_url)
        logging.debug('Successfully parsed DSIT announcements')
    except requests.exceptions.RequestException:
        logging.error(f'Could not reach DSIT announcement page using {announcements_url}')

    return announcements


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
        # Date parsing
        date_str = announcement.find('span', attrs={'class': 'updated'})

        # The actual time we get from the DSIT announcement page is in Athens timezone, however the provided one,
        # using %z, is UTC. We fix that using .replace
        date_time_obj = datetime.datetime.strptime(date_str.text, '%Y-%m-%dT%H:%M:%S%z') \
            .replace(tzinfo=pytz.timezone('Europe/Athens'))

        # Dates are surprisingly not ordered since we extract the last update time and not posting time
        converted_datetime = date_time_obj.strftime("%d-%m-%Y %H:%M")

        # Announcement link parsing
        href = announcement.find_all('a')[1]['href']

        # Title Parsing
        title = announcement.find_all('a')[1].contents[0]

        return title, converted_datetime, href, "DSIT"

    announcements = [Announcement(*parse_announcement(article)) for article in articles]

    return announcements
