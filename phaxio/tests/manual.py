import os

from phaxio import PhaxioApi

def main():

    print('This function will attempt to communicate with Phaxio to run \n'
        'some tests. You will need a valid API key and secret. Please\n'
        "ensure that you're using credentials for Phaxio's test (and not\n"
        "live) service."
    )

    """
    key = raw_input('Enter test API key: ')
    secret = raw_input('Enter secret: ')
    """

    key = '20df64effed2a34e33afbaf1e40e044384b3fad2'
    secret = '068460fc06fd7cb6ec0c3678766d91acc03b63b7'

    api = PhaxioApi(key, secret)

    print('Sending fax')
    r = api.send(to='4141234567',
        string_data='H' * 8000,
        string_data_type='text',
        batch_collision_avoidance=True)
    print('Test %s: %s\n' % (
        'PASSED' if r['success'] else 'FAILED', r['message']
    ))

    print('Requesting test receive')
    fn = os.path.join(os.path.dirname(__file__), 'llama.pdf')
    r = api.testReceive(filename = fn)
    print('Test %s: %s\n' % (
        'PASSED' if r['success'] else 'FAILED', r['message']
    ))


if __name__ == '__main__':
    main()
