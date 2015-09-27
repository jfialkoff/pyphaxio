import os
import time
import unittest

from phaxio import PhaxioApi

try:
    raw_input
except NameError:
    raw_input = input


class APITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(APITestCase, cls).setUpClass()

        key = raw_input('Enter test API key: ')
        secret = raw_input('Enter secret: ')

        cls.api = PhaxioApi(key, secret, raise_errors=True)

    def setUp(self):
        super(APITestCase, self).setUp()

        # Due to Phaxio's API rate limiting,
        # we will wait 1 second between each test
        time.sleep(1)

    def test_sending_long_fax(self):
        r = self.api.send(
            to='4147654321',
            string_data='Hello World! ' * 8000,
            string_data_type='text'
        )

        self.assertTrue(r['success'])

    def test_sending_multiple_recipients(self):
        r = self.api.send(
            to=['4147654321', '5147654321', '6157654321'],
            string_data='Hello World!',
            string_data_type='text'
        )

        self.assertTrue(r['success'])

    def test_sending_files(self):
        llama = os.path.join(os.path.dirname(__file__), 'llama.pdf')
        alpaca = os.path.join(os.path.dirname(__file__), 'alpaca.pdf')
        f = open(alpaca, 'rb')
        r = self.api.send(to='4147654321', files=(llama, f))

        self.assertTrue(r['success'])

    def test_receive(self):
        llama = os.path.join(os.path.dirname(__file__), 'llama.pdf')
        r = self.api.testReceive(files=llama)

        self.assertTrue(r['success'])

    def test_fax_status(self):
        r = self.api.send(
            to='4147654321',
            string_data='Hello World!',
            string_data_type='text'
        )
        fax_id = r.get('faxId')

        r = self.api.faxStatus(id=fax_id)

        self.assertTrue(r['success'])

if __name__ == '__main__':
    unittest.main()
