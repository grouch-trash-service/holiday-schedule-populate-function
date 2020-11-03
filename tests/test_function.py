from unittest import TestCase
from unittest.mock import patch, MagicMock

from holiday import function
from schedule import TrashScheduleService


class Test(TestCase):
    @patch('trash.holidayschedule')
    def test_lambda_handler(self, mock):
        new_holiday_schedule = {
            'Memorial Day': 'Routes delayed one day all week.',
        }

        old_holiday_schedule = {
            'data': [{
                'name': 'Memorial Day',
                'routeDelays': 'No Delays'
            }, {
                'name': 'Easter',
                'routeDelays': 'No Trash on Sunday'
            }]
        }

        mock.return_value = new_holiday_schedule
        trash_service = TrashScheduleService('https://trash.com/api')
        trash_service.list = MagicMock(return_value=old_holiday_schedule)
        trash_service.update = MagicMock()
        trash_service.delete = MagicMock()
        function.trash_service = trash_service

        function.lambda_handler({}, {})
        self.assertTrue(mock.called)
        self.assertTrue(trash_service.list.called)
        trash_service.update.assert_called_with({'name': 'Memorial Day', 'routeDelays': 'Routes delayed one day all '
                                                                                        'week.'})
        trash_service.delete.assert_called_with('Easter')
