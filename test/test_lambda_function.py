import unittest

from lambda_function import lambda_handler


class TestLambdaFunction(unittest.TestCase):
    def test_lambda_handler(self):
        event = {'k': 'v'}
        lambda_handler(event, None)
        #assert ('g' == 'h')
