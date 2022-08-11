# cli.py

import argparse
# import json
import requests

def read_cli_arg():
    '''
    read command line args
    '''
    parser = argparse.ArgumentParser(
        prog='urlcheck', description='check connection status of url(s)',
        # exit_on_error=False
    )
    parser.add_argument(
        '-u',
        '--urls',
        metavar='URLs',
        nargs='+',
        type=str,
        default=[],
        help='enter one or more URLs to check their connection status',
    )
    parser.add_argument(
        '-f',
        '--input-file',
        metavar='FILE',
        type=str,
        default='',
        help='read URLs from a file',
    )
    parser.add_argument(
        '-a',
        '--asynchronous',
        action='store_true',
        help='check connectivity asynchronously',
    )
    parser.add_argument(
        '-s',
        '--scrape',
        type=str,
        default='',
        help='scrapes all url data from given webpage',
    )
    parser.add_argument(
        '-r',
        '--request',
        action='store_true',
        help='use with --scrape to request status code of all urls on scraped page',
    )
    return parser.parse_args()

def show_results(result, url, error=''):
    '''
    prints program output to terminal
    '''
    if result:
        print('🟢 Online ~~', end=' ')
    else:
        print(f'❌ Unavailable\n\tError: "{error}"', end=' ')
    print(f'"{url}"')

def show_response(url, error=None):
    '''
    prints program output to terminal if requests option was selected
    '''
    try:
        response = requests.get(url)
        if response:
            print(f'🟢 Status {response.status_code} ~~', end=' ')
        else:
            print(f'❌ Unavailable \n\tError: "{response.status_code}"', end=' ')
    except Exception as e:
        error=str(e)
    # handle exceptions
    if error:
        print(f'❌ Unavailable \n\tError: "{error}"', end=' ')
    print(f'"{url}"')
