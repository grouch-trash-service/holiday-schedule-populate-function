"""
function module for invoking lambda function to populate holiday schedule for trash pickup.
"""
import logging
import logging.config
import configparser
import os
from typing import List
import trash
from schedule import TrashScheduleService

config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
config = configparser.ConfigParser()
config.read(config_file)

logging.config.fileConfig(config_file)

trash_service = TrashScheduleService(config['DEFAULT']['TrashScheduleServiceUrl'])


def lambda_handler(event, context):
    """
    lambda function for populating trash holiday schedule
    :param event: lambda event
    :param context: lambda context
    """
    logging.info('Starting function with context=%s and event=%s', context, event)
    holiday_schedule = trash.holidayschedule()
    old_holiday_schedule = trash_service.list()['data']
    old_holidays = [old_holiday['name'] for old_holiday in old_holiday_schedule]
    logging.info('Updating holiday schedule with schedule=%s', holiday_schedule)
    update_schedule(old_holidays, holiday_schedule)


def update_schedule(old_holidays: List[str], new_holidays: dict):
    """
    updates the trash holiday schedule with the new holidays
    :param old_holidays: list of old holiday names
    :param new_holidays:  new holidays to be updated
    """
    for holiday in new_holidays:
        trash_service.update({'name': holiday, 'routeDelays': new_holidays[holiday]})
        if holiday in old_holidays:
            old_holidays.remove(holiday)
    delete_holidays(old_holidays)


def delete_holidays(holidays: List[str]):
    """
    deletes a holiday
    :param holidays: list of holiday names to delete.
    """
    for holiday in holidays:
        trash_service.delete(holiday)


if __name__ == "__main__":
    lambda_handler(None, None)
