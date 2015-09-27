import time
import unittest

from phaxio import PhaxioApi
from phaxio.exceptions import AuthenticationError, APIError

try:
    raw_input
except NameError:
    raw_input = input


class ErrorHandlingTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(ErrorHandlingTestCase, cls).setUpClass()

        cls.key = raw_input('Enter test API key: ')
        cls.secret = raw_input('Enter secret: ')

    def setUp(self):
        super(ErrorHandlingTestCase, self).setUp()

        # Due to Phaxio's API rate limiting,
        # we will wait 1 second between each test
        time.sleep(1)

    def test_valid_request(self):
        api = PhaxioApi(self.key, self.secret, raise_errors=True)
        response = api.send(to='8138014253', string_data='test')
        self.assertTrue(response['success'])

    def test_authentication_error(self):
        api = PhaxioApi('invalid_key', 'invalid_secret', raise_errors=True)
        self.assertRaises(AuthenticationError, api.send, to='8138014253', string_data='test')

    def test_api_error(self):
        api = PhaxioApi(self.key, self.secret, raise_errors=True)
        self.assertRaises(APIError, api.send, to='invalid_number', string_data='test')

    def test_raise_errors_option(self):
        api = PhaxioApi(self.key, self.secret, raise_errors=False)
        response = api.send(to='invalid_number', string_data='test')

        self.assertFalse(response['success'])


if __name__ == '__main__':
    unittest.main()
