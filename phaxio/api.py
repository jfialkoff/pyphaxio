import collections
import requests

from .utils import curry
from .exceptions import AuthenticationError, APIError, ServerError

try:
    basestring
except NameError:
    basestring = str

class PhaxioApi(object):
    VERSION = 1
    BASE_URL = 'https://api.phaxio.com'
    __IMPLEMENTED = ('send', 'testReceive', 'attachPhaxCodeToPdf',
        'createPhaxCode', 'getHostedDocument', 'provisionNumber',
        'releaseNumber', 'numberList', 'faxFile', 'faxList',
        'faxStatus', 'faxCancel', 'accountStatus'
    )

    api_key = None
    api_secret = None

    def __init__(self, key, secret, raise_errors=False):
        """Construct a Phaxio API object

        :param key: Phaxio api key
        :param secret: Phaxio api secret
        :param raise_errors: If set to False (default)
            an api call will return the json response
            as it did previously. If set to True, an api
            call will now raise an appropriate error.
        """
        self.api_key = key
        self.api_secret = secret
        self._raise_errors = raise_errors

    def parse_response(self, response):
        """Parses the API response and raises appropriate
        errors if raise_errors was set to True

        :param response: response from requests http call
        :returns: dictionary of response
        :rtype: dict
        """
        payload = None
        if isinstance(response.json, collections.Callable):
            payload = response.json()
        else:
            # json isn't callable in old versions of requests
            payload = response.json

        if not self._raise_errors:
            return payload
        else:
            if response.status_code == 401:
                raise AuthenticationError(payload['message'])
            elif response.status_code == 500:
                raise ServerError(payload['message'])
            elif not payload['success']:
                raise APIError(payload['message'])
            else:
                return payload

    def _get(self, method, **kwargs):
        """Builds the url for the specified method and arguments and returns
        the response as a dictionary.
        """

        payload = kwargs.copy()
        payload['api_key'] = self.api_key
        payload['api_secret'] = self.api_secret

        to = payload.pop('to', None)
        if to:
            if isinstance(to, basestring):
                payload['to'] = to
            else:
                # Presumably it's a list or tuple
                for num_i, fax_num in enumerate(to):
                    payload['to[%d]' % num_i] = fax_num

        files = payload.pop('files', [])
        if not isinstance(files, (list, tuple)): files = (files,)

        req_files = {}
        for file_i, f in enumerate(files):
            if isinstance(f, basestring):
                req_files['filename[%d]' % file_i] = open(f, 'rb')
            else:
                f.seek(0)
                req_files['filename[%d]' % file_i] = f

        url = '%s/v%d/%s' % (self.BASE_URL, self.VERSION, method)

        r = requests.post(url, data=payload, files=req_files)

        return self.parse_response(r)

    def __getattribute__(self, name):
        if name in PhaxioApi.__IMPLEMENTED:
            return curry(self._get, name)
        return super(PhaxioApi, self).__getattribute__(name)
