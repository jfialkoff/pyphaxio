import os

from phaxio import PhaxioApi

try:
    raw_input
except NameError:
    raw_input = input

def main():

    print('This function will attempt to communicate with Phaxio to run \n'
        'some tests. You will need a valid API key and secret. Please\n'
        "ensure that you're using credentials for Phaxio's test (and not\n"
        "live) service."
    )

    key = raw_input('Enter test API key: ')
    secret = raw_input('Enter secret: ')

    api = PhaxioApi(key, secret)

    print('Sending long fax to multiple recipients with string data')
    r = api.send(to=['4141234567', '5141234567', '6151234567'],
        string_data='Hello World! ' * 8000,
        string_data_type='text')
    faxId = r.get('faxId')
    print('Test %s: %s\n' % (
        'PASSED' if r['success'] else 'FAILED', r['message']
    ))

    print('Sending fax with files')
    llama = os.path.join(os.path.dirname(__file__), 'llama.pdf')
    alpaca = os.path.join(os.path.dirname(__file__), 'alpaca.pdf')
    f = open(alpaca, 'rb')
    r = api.send(to='4141234567', files=(llama, f))
    print('Test %s: %s\n' % (
        'PASSED' if r['success'] else 'FAILED', r['message']
    ))

    print('Requesting test receive')
    r = api.testReceive(files = llama)
    print('Test %s: %s\n' % (
        'PASSED' if r['success'] else 'FAILED', r['message']
    ))

    if not faxId:
        print('Skipping test 4 because test 1 failed.')
    else:
        print('Get fax status')
        r = api.faxStatus(id = faxId)
        print('Test %s: %s\n' % (
            'PASSED' if r['success'] else 'FAILED', r['message']
        ))

if __name__ == '__main__':
    main()
