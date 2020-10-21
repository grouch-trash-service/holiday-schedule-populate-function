from unittest import TestCase
from holiday import function


class Test(TestCase):
    def test_lambda_handler(self):
        function.lambda_handler({}, {})
