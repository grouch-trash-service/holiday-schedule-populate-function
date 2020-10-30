import unittest
import boto3
import requests
from unittest.mock import patch, MagicMock

from aws_requests_auth.aws_auth import AWSRequestsAuth
from botocore.credentials import Credentials

from holiday.schedule import TrashScheduleService


class TestCase(unittest.TestCase):

    def setUp(self):
        self.trash_schedule_service = TrashScheduleService('https://test.amazonaws.com/Prod/v1/holidays')
        self.auth = AWSRequestsAuth(aws_access_key='ACCESS_KEY',
                                    aws_secret_access_key='SECRET',
                                    aws_host='test.amazonaws.com',
                                    aws_region='us-east1',
                                    aws_service='execute-api')

    @patch('boto3.Session')
    def test_get_auth(self, test_patch):
        expected_credentials = Credentials('ACCESS_KEY', 'SECRET')
        session = TestCase.__mock_boto3_session(expected_credentials)
        test_patch.return_value = session

        expected_auth = self.auth

        auth = self.trash_schedule_service._get_auth()

        self.assertEqual(expected_auth.aws_access_key, auth.aws_access_key)
        self.assertEqual(expected_auth.aws_secret_access_key, auth.aws_secret_access_key)
        self.assertEqual(expected_auth.aws_host, auth.aws_host)
        self.assertEqual(expected_auth.aws_region, auth.aws_region)

    @patch('requests.put')
    def test_update(self, mock):
        holiday = {'name': 'Christmas', 'routeDelays': 'No Delays'}
        self.trash_schedule_service.update(holiday)
        self.assertTrue(mock.called)

    @patch('requests.delete')
    def test_delete(self, mock):
        holiday = 'Christmas'
        self.trash_schedule_service.delete(holiday)
        self.assertTrue(mock.called)

    @patch('requests.get')
    def test_list(self, mock):
        response = requests.Response()
        data = {
            'data': [{
                'name': 'Programmer Day',
                'routeDelays': 'None!'
            }]
        }
        response.json = MagicMock(return_value=data)
        mock.return_value = response
        holidays = self.trash_schedule_service.list()
        self.assertEqual(data, holidays)

    @staticmethod
    def __mock_boto3_session(credentials):
        session = boto3.Session()
        credentials.get_frozen_credentials = MagicMock(return_value=credentials)
        session.get_credentials = MagicMock(return_value=credentials)
        session.region_name = 'us-east1'
        return session


if __name__ == '__main__':
    unittest.main()
