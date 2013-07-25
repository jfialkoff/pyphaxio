import requests
import urllib

from .utils import curry

class PhaxioApi(object):
    VERSION = 1
    BASE_URL = 'https://api.phaxio.com'
    __IMPLEMENTED = ('send', 'testReceive', 'attachPhaxCodeToPdf',
        'createPhaxCode', 'getHostedDocument'
    )

    api_key = None
    api_secret = None

    def __init__(self, key, secret):
        self.api_key = key
        self.api_secret = secret

    def _get(self, method, **kwargs):
        """ Builds the url for the specified method and arguments and returns
        the response as a dictionary.
        """

        payload = kwargs.copy()
        payload['api_key'] = self.api_key
        payload['api_secret'] = self.api_secret
        payload = '&'.join(
            ['%s=%s' % (key, urllib.quote(unicode(val), ''))
            for key, val in payload.items()]
        )
        url = '%s/v%d/%s?%s' % (self.BASE_URL, self.VERSION, method,
            payload)
        print(url)
        r = requests.get(url)
        return r.json()

    def __getattribute__(self, name):
        if name in PhaxioApi.__IMPLEMENTED:
            return curry(self._get, name)
        return super(PhaxioApi, self).__getattribute__(name)


