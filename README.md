# Phaxio

A Python module for interacting with the [Phaxio API]( https://www.phaxio.com/docs ).

## Installation

Via pip:

    $ pip install pyphaxio

## Usage

Send a fax to multiple people using HTML message:

    api = PhaxioApi(key, secret)
    r = api.send(to=['4141234567', '5141234567', '6151234567'],
        string_data='Hello World!',
        string_data_type='text')
    print(r.get('faxId'))

Generally, each supported method takes keyword arguments with the exact same
names of the API method parameters as they're described in the
[documentation](https://www.phaxio.com/docs). One exception to this rule is that
`filename` is instead referred to as `files`. For example, to send a fax using
files:

    llama = os.path.join(os.path.dirname(__file__), 'tests/llama.pdf')
    alpaca = os.path.join(os.path.dirname(__file__), 'tests/alpaca.pdf')
    f = open(alpaca, 'rb')
    r = api.send(to='4141234567', files=(llama, f))

See the [manual tests](phaxio/test/manual.py) for additional examples.

### Currently Supported API Calls

Implemented and tested:

* send
* testReceive
* faxStatus

Implemented and untested:

* attachPhaxCodeToPdf
* createPhaxCode
* getHostedDocument
* provisionNumber
* releaseNumber
* numberList
* faxFile
* faxList
* faxCancel
* accountStatus

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Added some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
