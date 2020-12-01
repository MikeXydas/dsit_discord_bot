from bs4 import BeautifulSoup

import requests
import logging
import datetime
import pytz

from dsit_bot.settings import bot_settings
from dsit_bot.announcements.announcements_sender import Announcement


def initialize_uoa_dit_announcements():
    """
    Initializes a list of announcements that are requested and parsed from the UoA DIT announcements page.

    Returns:
        A list of Announcement objects
    """
    announcements_url = bot_settings['announcements']['url_DIT']
    announcements = None
    try:
        logging.debug('Requesting announcements from DSIT announcement page')
        announcements = parse_dit_uoa_announcements(announcements_url)
        logging.debug('Successfully parsed UoA DIT announcements')
    except requests.exceptions.RequestException:
        logging.error(f'Could not reach UoA DIT announcement page using {announcements_url}')

    return announcements


def parse_dit_uoa_announcements(url):
    """
    Creates a list of Announcement objects parsed from the announcements page of the DSIT homepage.

    Args:
        url: The url of the announcements page, currently: https://www.di.uoa.gr/announcements

    Returns:
        A list of Announcement objects

    Raises:
        requests.exceptions.RequestException: If we fail to connect to the DSIT announcement page
    """
    try:
        resp = requests.get(url)
        resp.raise_for_status()  # Raising request exception if status code is not 200
    except requests.exceptions.RequestException as e:
        logging.error('Failed to reach UoA DIT announcements page')
        raise e

    announce_soup = BeautifulSoup(resp.text, features="html.parser")
    ann_table = announce_soup.find('table', attrs={'class': 'table table-hover cols-4'})
    all_announcements = ann_table.find('tbody').find_all('tr')

    # print(all_announcements)

    def parse_announcement(announcement):
        # Title and Link parsing
        title_link = announcement.find('h5').find('a')
        link = "https://www.di.uoa.gr" + title_link['href']
        title = title_link.contents[0]

        # Date Parsing
        date_str = announcement\
            .find('td', attrs={'class': 'date views-field views-field-created'})\
            .contents[0].strip()

        # Category Parsing
        categories_list = announcement\
            .find('td', attrs={'class': 'category views-field views-field-field-news-category'}) \
            .contents
        categories_str = ''.join(str(categories_list))

        return (title, date_str, link, "DIT"), categories_str

    def is_in_filters(ann_categories):
        cat_filters = ['Μεταπτυχιακά']  # Hardcoded filters allowed
        if any(cat_filter in ann_categories for cat_filter in cat_filters):
            return True

    returned_announcements = []
    for ann in all_announcements:
        ann_content, categories = parse_announcement(ann)
        if is_in_filters(categories):
            returned_announcements.append(Announcement(*ann_content))

    return returned_announcements
