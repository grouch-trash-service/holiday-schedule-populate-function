"""
Module for updating trash holiday schedule
"""

from urllib.parse import urlparse

import boto3
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth
from botocore.credentials import Credentials


class TrashScheduleService:
    """
    TrashScheduleService is a service class that updates the trash holiday schedule
    """

    def __init__(self, url: str):
        self.url = url

    @staticmethod
    def __get_credentials() -> Credentials:
        session = boto3.Session()
        credentials = session.get_credentials()
        return credentials.get_frozen_credentials()

    def _get_auth(self) -> AWSRequestsAuth:
        host = urlparse(self.url).netloc
        credentials = TrashScheduleService.__get_credentials()
        return AWSRequestsAuth(aws_access_key=credentials.access_key,
                               aws_secret_access_key=credentials.secret_key,
                               aws_token=credentials.token,
                               aws_host=host,
                               aws_region=boto3.Session().region_name,
                               aws_service='execute-api')

    def update(self, holiday: dict):
        """
        updates holiday
        :param holiday: dict containing name of holiday and route delays
        """
        auth = self._get_auth()
        data = {
            'data': holiday
        }
        requests.put(self.url+"/{name}".format(name=holiday['name']),json=data, auth=auth)

    def delete(self, holiday: str):
        """
        deletes holiday
        :param holiday: name of the holiday to delete
        """
        auth = self._get_auth()
        requests.delete(self.url+f"/{holiday}", auth=auth)

    def list(self) -> dict:
        """
        lists all holiday schedules
        :return:  dict with holiday schedule information.
        """
        auth = self._get_auth()
        response = requests.get(self.url, auth=auth)
        return response.json()
