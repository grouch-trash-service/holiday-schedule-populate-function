"""
trash module for extracting holiday schedule from trash service.
"""
import os
import configparser
import requests
import holidays
from lxml import html


config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
config = configparser.ConfigParser()
config.read(config_file)

TRASH_SERVICE_URL = config['DEFAULT']['TrashServiceUrl']
us_holidays = holidays.UnitedStates()


def holidayschedule() -> dict:
    """
    gets the trash holiday schedule
    :return: a dict with holiday as the key and route delays as the value
    """
    holiday_list = __parse_page_content()
    holiday_list = [date.split('-')[0] for date in holiday_list]
    trash_schedule = __parse_holiday_list(holiday_list)
    return trash_schedule


def __parse_page_content() -> list:
    page = requests.get(TRASH_SERVICE_URL)
    tree = html.fromstring(page.content)
    return tree.xpath('//div[@id="content"]//span/text()')[1:]


def __parse_holiday_list(holiday_list: list) -> dict:
    trash_schedule = {}
    for i in range(0, len(holiday_list), 2):
        if holiday_list[i] in us_holidays:
            holiday = us_holidays.get(holiday_list[i])
            trash_schedule[holiday] = holiday_list[i + 1]
    return trash_schedule
