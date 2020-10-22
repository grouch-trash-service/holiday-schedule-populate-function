import unittest
import os
from unittest.mock import patch, MagicMock
from holiday import trash


class TestCase(unittest.TestCase):
    @patch('requests.get')
    def test_holidayschedule(self, test_request):
        response = Response()
        trash_html = os.path.join(os.path.dirname(__file__), 'trash.html')
        response.content = open(trash_html).read()
        test_request.return_value = response
        expected_schedule = {
            'Memorial Day': 'Routes delayed one day all week.',
            'Independence Day': 'No Delays.',
            'Labor Day': 'Routes delayed one day all week.',
            'Thanksgiving': 'Routes delayed one day Thursday and Friday only.',
            'Christmas Day': 'Routes delayed Friday only.',
            "New Year's Day": 'Routes delayed Friday only.'
        }

        holiday_schedule = trash.holidayschedule()
        self.assertEqual(expected_schedule, holiday_schedule)


class Response:
    pass


if __name__ == '__main__':
    unittest.main()
